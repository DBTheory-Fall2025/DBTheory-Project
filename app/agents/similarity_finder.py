from ..ai_setup import model_stream, model
from ..utils.agent_util import stream_agent_message, send_agent_update, send_sql_result
from ..utils.db_util import get_enhanced_schema
from ..utils.mermaid_util import generate_schema_diagram
from .sql_error_handler import read_sql_safely
import json
import hashlib

# Constants
READ_REQUEST_TEMPLATE = """{
  "read_requests": [
    {"db": "db1", "query": "SELECT * FROM users LIMIT 5"},
    {"db": "db2", "query": "SELECT * FROM members LIMIT 5"}
  ]
}"""

ANALYSIS_STRUCTURE = """
Overview:
[High level summary]

Mergeable Tables:
- [Table A] and [Table B] -> [Unified Table]
  - Logic: ...

Standardization Opportunities:
- [Column X] and [Column Y] -> [Unified Column]

Unmergeable Tables:
- [Table C] (Keep as is)
"""

def find_similarities(db_connections, status_callback=None):
    """
    Analyzes schemas to find similarities using AI.
    """
    schemas = _pull_schemas(db_connections, status_callback)
    _generate_diagram(schemas, status_callback)
    
    prompt = _build_initial_prompt(schemas)
    
    # Get initial analysis (potentially containing JSON request)
    ai_response = _get_ai_response_safely(prompt, "similarity-finder", "A", status_callback)
    analysis = ai_response

    # Check for data read requests
    request_obj = _parse_json_request(ai_response)
    
    if request_obj:
        # Process requests and get samples
        data_samples = _process_data_requests(db_connections, request_obj, schemas, status_callback)
        
        # Re-analyze with data
        analysis = _run_final_analysis(data_samples, status_callback)

    return analysis

def _pull_schemas(db_connections, status_callback):
    send_agent_update("similarity-finder", "Pulling schema information...", "A", status_callback=status_callback)
    schemas = {}
    for db_name, conn in db_connections.items():
        schemas[db_name] = get_enhanced_schema(conn)
        print(f"[DEBUG] Schema returned for {db_name}: {schemas[db_name].keys()}", flush=True)
    
    if not any(schemas.values()):
        raise Exception("No schemas found in the selected databases.")
    return schemas

def _generate_diagram(schemas, status_callback):
    try:
        diagram = generate_schema_diagram(schemas)
        send_agent_update("similarity-finder", f"\n```mermaid\n{diagram}\n```\n", "A", status_callback=status_callback)
    except Exception as e:
        print(f"Error generating diagram: {e}")

def _build_initial_prompt(schemas):
    schema_text = ""
    for db_name, schema_info in schemas.items():
        schema_text += f"Database: {db_name}\n"
        for table_name, details in schema_info.items():
            schema_text += f"  Table: {table_name}\n"
            for col_name, col_type in details['columns'].items():
                extras = []
                if col_name in details['pks']:
                    extras.append("PK")
                for fk in details['fks']:
                    if fk['col'] == col_name:
                        extras.append(f"FK -> {fk['ref_table']}.{fk['ref_col']}")
                extra_str = f" [{', '.join(extras)}]" if extras else ""
                schema_text += f"    - {col_name} ({col_type}){extra_str}\n"
        schema_text += "\n"

    return f"""
You are an advanced data engineer tasked with merging two databases. Please analyze these schemas and identify columns and tables that are similar and could be merged.
You can request to see sample data from specific tables to help with your analysis.

Here are the schemas:
{schema_text}

If you want to see actual sample data to help with your analysis, respond ONLY with a JSON object like this:

{READ_REQUEST_TEMPLATE}

If you have enough information already, provide your detailed analysis and reasoning in PLAIN TEXT (Markdown allowed). 
Do NOT wrap your final analysis in JSON. Structure your analysis clearly.

Recommended structure:
{ANALYSIS_STRUCTURE}
"""

def _get_ai_response_safely(prompt, agent_name, node_id, status_callback):
    """
    Streams response but hides it if it starts with JSON.
    """
    generator = model_stream(prompt, agent_name=agent_name)
    first_chunk = next(generator, None)
    
    if not first_chunk:
        return ""

    stripped = first_chunk.strip()
    # Check for JSON start
    is_json = stripped.startswith('{') or stripped.startswith('```json') or (stripped.startswith('```') and not stripped.startswith('```mermaid'))
    
    full_response = first_chunk
    
    if is_json:
        # Buffer silently
        for chunk in generator:
            full_response += chunk
        return full_response
    else:
        # Stream visibly
        def reconstructed_gen():
            yield first_chunk
            yield from generator
            
        return stream_agent_message(
            agent_id=agent_name,
            node_id=node_id,
            message_generator_or_callable=reconstructed_gen,
            status_callback=status_callback,
            is_code=False
        )

def _parse_json_request(text):
    if not isinstance(text, str) or '"read_requests"' not in text:
        return None
    
    try:
        clean = text.strip()
        if clean.startswith("```json"): clean = clean[7:]
        if clean.startswith("```"): clean = clean[3:]
        if clean.endswith("```"): clean = clean[:-3]
        return json.loads(clean.strip())
    except json.JSONDecodeError:
        print("Failed to parse JSON request from AI.")
        return None

def _process_data_requests(db_connections, request_obj, schemas, status_callback):
    send_agent_update("similarity-finder", "Getting table content...", "A", status_callback=status_callback)
    data_samples = {}
    
    for req in request_obj.get("read_requests", []):
        db_name = req.get("db")
        original_query = req.get("query")
        
        if not db_name or not original_query:
            continue
            
        if db_name not in db_connections:
            # We still need to show an error message manually if DB is unknown
            msg_hash = hashlib.md5(f"{db_name}:{original_query}".encode()).hexdigest()
            message_id = f"result-{msg_hash}"
            send_sql_result("similarity-finder", db_name, original_query, "Error: Unknown database", "A", status_callback, message_id)
            continue

        conn = db_connections[db_name]
        schema_context = schemas.get(db_name)
        
        # Use safe execution with auto-fix
        result = read_sql_safely(
            conn=conn, 
            query=original_query, 
            agent_name="similarity-finder", 
            status_callback=status_callback, 
            schema_context=schema_context, 
            db_name=db_name,
            node_id="A"
        )

        if result:
            data_samples[f"{db_name}:{original_query}"] = result
        else:
            data_samples[f"{db_name}:{original_query} (Failed)"] = "Failed to fetch data."
            
    return data_samples


def _run_final_analysis(data_samples, status_callback):
    try:
        data_json = json.dumps(data_samples, indent=2, default=str)
    except Exception as e:
        print(f"Error serializing data samples to JSON: {e}", flush=True)
        data_json = str(data_samples)

    re_prompt = f"""
Here are the results of your requested queries:

{data_json}

Now re-analyze the schemas using this data context,
and provide your final similarity analysis and merge plan in PLAIN TEXT (Markdown allowed).
Do NOT wrap it in JSON.

Recommended structure:
{ANALYSIS_STRUCTURE}
"""
    return stream_agent_message(
        agent_id="similarity-finder",
        node_id="A",
        message_generator_or_callable=lambda: model_stream(re_prompt, agent_name="similarity_finder"),
        status_callback=status_callback,
        is_code=False
    )
