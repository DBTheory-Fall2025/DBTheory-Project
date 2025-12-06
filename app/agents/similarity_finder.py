from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message, send_agent_update
from ..utils.db_util import get_enhanced_schema, read_sql_data, read_sql_data_with_headers
from ..utils.mermaid_util import generate_schema_diagram
import json

read_request = """{
  "read_requests": [
    {"db": "db1", "query": "SELECT * FROM users LIMIT 5"},
    {"db": "db2", "query": "SELECT * FROM members LIMIT 5"}
  ]
}"""

# We no longer enforce JSON for the final analysis, but we give a structure hint
analysis_structure = """
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
    Analyzes the schemas of the given databases and uses an AI model
    to find similarities between them.
    """
    schemas = {}
    
    # 1. Pull Schema Information
    send_agent_update("similarity-finder", "Pulling schema information...", "A", status_callback=status_callback)
    
    for db_name, conn in db_connections.items():
        # Use enhanced schema to get PKs/FKs
        schema = get_enhanced_schema(conn)
        print(f"[DEBUG] Schema returned for {db_name}: {schema.keys()}", flush=True)
        schemas[db_name] = schema

    # Failsafe: If no schemas or empty schemas, abort
    if not any(schemas.values()):
        error_msg = "No schemas found in the selected databases. Aborting AI analysis."
        print(f"[ERROR] {error_msg}")
        raise Exception(error_msg)

    # 2. Generate and send Mermaid Diagram
    try:
        diagram = generate_schema_diagram(schemas)
        send_agent_update("similarity-finder", f"\n```mermaid\n{diagram}\n```\n", "A", status_callback=status_callback)
    except Exception as e:
        print(f"Error generating diagram: {e}")

    # Format the schemas into a prompt for the AI
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

    prompt = f"""
You are an advanced data engineer tasked with merging two databases. Please analyze these schemas and identify columns and tables that are similar and could be merged.
You can request to see sample data from specific tables to help with your analysis.

Here are the schemas:
{schema_text}

If you want to see actual sample data to help with your analysis, respond ONLY with a JSON object like this:

{read_request}

If you have enough information already, provide your detailed analysis and reasoning in PLAIN TEXT (Markdown allowed). 
Do NOT wrap your final analysis in JSON. Structure your analysis clearly.

Recommended structure:
{analysis_structure}
"""

    # Get the AI's response
    ai_response = stream_agent_message(
        agent_id="similarity-finder",
        node_id="A",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="similarity_finder"),
        status_callback=status_callback,
        is_code=False
    )
    analysis = ai_response

    # Check if the AI requested data (JSON format)
    if isinstance(ai_response, str) and '"read_requests"' in ai_response:
        errors_occurred = False
        data_samples = {}
        try:
            # Clean possible markdown fences
            clean_response = ai_response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
            
            request_obj = json.loads(clean_response.strip())
        except json.JSONDecodeError as e:
            # If it's not valid JSON, assume it's the text analysis and proceed
            print(f"JSON decode error or text response: {e}")
            return analysis

        # 3. Getting Table Content
        send_agent_update("similarity-finder", "Getting table content...", "A", status_callback=status_callback)

        for req in request_obj.get("read_requests", []):
            db_name = req.get("db")
            query = req.get("query")

            if not db_name or not query:
                continue
            if db_name not in db_connections:
                data_samples[f"{db_name}:{query}"] = "Error: unknown database name"
                errors_occurred = True
                continue

            try:
                result = read_sql_data_with_headers(db_connections[db_name], query)
                data_samples[f"{db_name}:{query}"] = result
            except Exception as e:
                data_samples[f"{db_name}:{query}"] = f"Error executing query: {e}"
                errors_occurred = True

        # 4. Show Queries and Results
        # Generate HTML for side-by-side view
        results_html = '<div class="query-results-container">'
        for key, result in data_samples.items():
            parts = key.split(':', 1)
            db = parts[0]
            query_str = parts[1] if len(parts) > 1 else "Unknown Query"
            
            # Generate table
            table_html = ""
            if isinstance(result, dict) and 'columns' in result:
                cols = result['columns']
                rows = result['rows']
                
                table_html = '<table class="result-table"><thead><tr>'
                for col in cols:
                    table_html += f'<th>{col}</th>'
                table_html += '</tr></thead><tbody>'
                
                # Limit rows for display if too many?
                for row in rows[:10]: # Display top 10 rows
                    table_html += '<tr>'
                    for cell in row:
                        table_html += f'<td>{str(cell)}</td>'
                    table_html += '</tr>'
                if len(rows) > 10:
                    table_html += f'<tr><td colspan="{len(cols)}">... ({len(rows)-10} more rows) ...</td></tr>'
                table_html += '</tbody></table>'
            else:
                table_html = f'<div class="error">{result}</div>'
                
            results_html += f'''
            <div class="query-result-row">
                <div class="query-box">
                    <h4>Query ({db})</h4>
                    <pre>{query_str}</pre>
                </div>
                <div class="result-box">
                    <h4>Result</h4>
                    {table_html}
                </div>
            </div>
            '''
        results_html += '</div>'

        send_agent_update("similarity-finder", f"```html\n{results_html}\n```", "A", status_callback=status_callback)

        # Build the follow-up prompt
        re_prompt = f"""
Here are the results of your requested queries:

{json.dumps(data_samples, indent=2)}

Now re-analyze the schemas using this data context,
and provide your final similarity analysis and merge plan in PLAIN TEXT (Markdown allowed).
Do NOT wrap it in JSON.

Recommended structure:
{analysis_structure}
"""

        analysis = stream_agent_message(
            agent_id="similarity-finder",
            node_id="A",
            message_generator_or_callable=lambda: model_stream(re_prompt, agent_name="similarity_finder"),
            status_callback=status_callback,
            is_code=False
        )

    return analysis
