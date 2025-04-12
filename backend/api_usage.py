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

    pre_sentence = "You are a licensed therapist helping people with mental health issues. Answer the following question with care. "
    combined_input = pre_sentence + user_input

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=combined_input)

    return  response.text
