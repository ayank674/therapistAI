from dotenv import load_dotenv
import os
from google import genai
from backend import db_formation

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

def ask_ai(user_input, user_id, user_data):

    conversation_history = user_data.get_cache(user_id) 

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=conversation_history + user_input)
    
    user_data.add_cache(user_id, "user", user_input)
    user_data.add_cache(user_id, "ai", response)

    return  response.text

def greet(user_id, user_data):
    user_data.clear_cache(user_id)
    pre_prompt = "You are acting as a licensed therapist helping people with mental health issues. It is understood that you are an ai and not licensed. Answer the following question with care and as if you are having a short conversation with a friend and remove any quotes in the response. Now greet me"

    response = client.models.generate_content(
            model="gemini-2.0-flash", contents=pre_prompt)
    
    user_data.add_cache(user_id, "ai", response)
    return  response.text

if __name__ == "__main__":
    print(ask_ai("Hello"))
