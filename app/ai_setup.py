from google import genai
#import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

#genai.configure(api_key=os.getenv("API_KEY"))
 
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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=history
    )


    history += f"Assistant: {response.text}\n"

    return response.text
print(model("hi"))