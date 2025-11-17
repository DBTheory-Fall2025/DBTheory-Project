from ..ai_setup import model_stream
from ..utils.agent_util import stream_agent_message

def check_logic(analysis, new_schema, sql_commands, conversion_scripts, status_callback=None):
    """
    Checks the logic of the generated assets such as the conversion scripts and new tables.
    """
    prompt = f"""
You are a senior data engineer reviewing the output of an automated database merging system.
Your job is to check for logical consistency across all generated assets.

Please analyze the following:
1. The similarity analysis of the source databases.
2. The new unified schema.
3. The generated CREATE TABLE statements.
4. The generated INSERT (conversion) scripts.

You must identify:
- Mismatched table or column names between schema and SQL statements.
- Data type mismatches (e.g., inserting text into numeric columns).
- Incorrect joins or key relationships.
- Missing fields or insert targets.
- Are foreign keys and primary keys handled correctly?
- Are there any obvious inconsistencies or contradictions?

Respond only with "True" if everything seems logically correct,
or "False" if any inconsistencies are found. Do not include any additional notations or comments.

Similarity Analysis:
{analysis}

New Schema:
{new_schema}

CREATE TABLE statements:
{sql_commands}

INSERT/Conversion scripts:
{conversion_scripts}

"""
    response = stream_agent_message(
        agent_id="logic-checker",
        node_id="I",
        message_generator_or_callable=lambda: model_stream(prompt, agent_name="logic_checker"),
        status_callback=status_callback,
        is_code=False
    ).strip().lower()

    if response == "true":
        return True
    elif response == "false":
        return False
    else:
        print(f"[logic_checker] Unexpected model response: {response}")
        return False
