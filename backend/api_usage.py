from dotenv import load_dotenv
import os
from google import generativeai as genai
from flask import Blueprint, request, jsonify


def ask_ai():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=key)

    data = request.get_json()
    user_input = data.get("input")

    pre_sentence = "You are acting as a licensed therapist helping people with mental health issues. It is understood that you are an ai and not licensed. Answer the following question with care and as if you are having a short conversation with a friend and remove any quotes in the response. "
    combined_input = pre_sentence + user_input

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=combined_input)

    return  response.text
