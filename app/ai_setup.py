import google.generativeai as genai
from dotenv import load_dotenv
import os

genai.configure(api_key=os.getenv("API_KEY"))
load_dotenv() 
client = genai.Client()

system_prompt = (
    "You are a helpful SQL data engineering agent. You will be provided with two databases and your task is to combine them."
    "Always generate valid SQL queries, and explain briefly what each query does."
)

# Conversation history
history = system_prompt + "\n\n"

def model(prompt):
    global history

    history += f"User: {prompt}\n"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(history)


    history += f"Assistant: {response.text}\n"

    return response.text
