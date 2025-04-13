from dotenv import load_dotenv
import os
from google import genai
from flask import Blueprint, request, jsonify

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

def ask_ai(user_input):

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_input)

    return  response.text

def greet():
    pre_prompt = "You are acting as a licensed therapist helping people with mental health issues. It is understood that you are an ai and not licensed. Answer the following questions with care and as if you are having a short conversation with a friend and remove any quotes in the response. Now greet me"

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=pre_prompt)

    return  response.text

if __name__ == "__main__":
    print(ask_ai("Hello"))
