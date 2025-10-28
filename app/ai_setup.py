import google.generativeai as genai
from dotenv import load_dotenv
import os

genai.configure(api_key=os.getenv("API_KEY"))

system_prompt = (
    "You are a helpful SQL data engineering agent. You will be provided with two databases and your task is to combine them."
    "Always generate valid SQL queries, and explain briefly what each query does."
)

# Conversation history
history = system_prompt + "\n\n"

_histories = {}

def model(user_prompt, agent_name="default"):
    """Same as before, but with separate memory per agent."""
    if agent_name not in _histories:
        _histories[agent_name] = [("system", system_prompt)]

    history = _histories[agent_name]
    history.append(("user", user_prompt))

    gm = genai.GenerativeModel("gemini-2.5-pro")
    response = gm.generate_content(
        "\n".join(f"{role}: {text}" for role, text in history)
    )

    text = response.text
    history.append(("assistant", text))
    return text

# def model(prompt):
#     global history

#     history += f"User: {prompt}\n"

#     model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
#     model = genai.GenerativeModel(model_name)
#     response = model.generate_content(history)


#     history += f"Assistant: {response.text}\n"

#     return response.text
