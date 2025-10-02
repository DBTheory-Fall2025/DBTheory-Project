from google import genai


client = genai.Client(api_key='AIzaSyB7j5JCVZWHKZwAO-P4Lx3Xm47LnHNk_vE')

system_prompt = (
    "You are a helpful SQL data engineering agent. You will be provided with two databases and your task is to combine them."
    "Always generate valid SQL queries, and explain briefly what each query does."
)

# Conversation history as a single evolving string
history = system_prompt + "\n\n"

def model(prompt):
    global history

    history += f"User: {prompt}\n"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history
    )


    history += f"Assistant: {response.text}\n"

    return response.text



prompt = f"""
Here are two database schemas:

Task: Write SQL queries that combine these databases. 
"""

print(model(system_prompt))
