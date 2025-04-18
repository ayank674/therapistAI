from dotenv import load_dotenv
import os
import psycopg
from psycopg2 import sql
# import api_usage

conn_url = os.getenv("PG_URI")

class UserData:

    def __init__(self, conn_url):
        self.conn = psycopg.connect(conn_url)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        

        # Create Demographics Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS demographics (
            user_id VARCHAR(100) PRIMARY KEY,
            password VARCHAR(225),
            name VARCHAR(100),
            age INT,
            gender VARCHAR(50),
            location VARCHAR(100),
            occupation VARCHAR(100),
            expectations VARCHAR(225)
            );
        """)

        # Create Cache Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cache (
            user_id VARCHAR(100) REFERENCES demographics(user_id) ON DELETE CASCADE,
            message_type VARCHAR(10),  -- 'user' or 'ai'
            message TEXT
            );
        """)
    
        self.conn.commit()

    def add_demographics(self, user_id: str, password: str):
        self.cursor.execute("""
            INSERT INTO demographics (user_id, password)
            VALUES (%s, %s)
            ON CONFLICT (user_id) 
            DO NOTHING;  -- Do nothing if the user already exists
        """, (user_id, password))
    
        self.conn.commit()
    
    def update_demographics(self, user_id: str, name: str, age: int, gender: str, location: str = None, occupation: str = None, expectations: str = None):
        self.cursor.execute("""
            UPDATE demographics
            SET name = %s, age = %s, gender = %s, location = %s, occupation = %s, expectations = %s 
            WHERE user_id = %s;
        """, (name, age, gender, location, occupation, expectations, user_id))
        
        self.conn.commit()

    def add_cache(self, user_id: str, message_type: str, message: str):
        self.cursor.execute("""
            INSERT INTO cache (user_id, message_type, message)
            VALUES (%s, %s, %s);
        """, (user_id, message_type, message))
        
        self.conn.commit()

    def get_demographics(self, user_id):
        self.cursor.execute("""
            SELECT user_id, password, name, age, gender, location, occupation, expectations
            FROM demographics
            WHERE user_id = %s;
        """, (user_id,))

        user_data = self.cursor.fetchone()

        if not user_data:
            return "User does not exist"
        
        return {
        "name": user_data[2],
        "age": user_data[3],
        "gender": user_data[4],
        "location": user_data[5],
        "occupation": user_data[6],
        "expectations": user_data[7]
        }

    def get_cache(self, user_id: str) -> str:
        self.cursor.execute("""
            SELECT message_type, message FROM cache WHERE user_id = %s;
        """, (user_id,))
        
        sessions = self.cursor.fetchall()

        if sessions:
            return [{"message_type": session[0], "message": session[1]} for session in sessions]
        else:
            return "No sessions found for this user."
        
    def get_messages(self, user_id: str):
        self.cursor.execute("""
            SELECT message FROM cache WHERE user_id = %s;
        """, (user_id,))
        messages = self.cursor.fetchall()
        return [msg[0] for msg in messages]
        
    def check_user(self, user_id, password):
        self.cursor.execute("""
            SELECT password FROM demographics WHERE user_id = %s AND password = %s;
        """, (user_id, password))

        stored_password = self.cursor.fetchone()

        return bool(stored_password)
    
    def clear_cache(self, user_id: str):
        self.cursor.execute("""
            DELETE FROM cache WHERE user_id = %s;
        """, (user_id,))
        
        self.conn.commit()

if __name__ == "__main__":
    user_data = UserData(os.getenv("PG_URI"))

    user_data.add_demographics(user_id="user123", password="password123")
    user_profile = user_data.get_demographics("user123")
    print(f"User profile: {user_profile}")

    user_data.update_demographics(
        user_id="user123", 
        password="password123", 
        name="John Doe", 
        age=30, 
        gender="Male", 
        location="New York", 
        occupation="Engineer",
        expectations="awesome"
    )

# Check user credentials
    is_authenticated = user_data.check_user(user_id="user123", password="password123")
    print(f"User authenticated: {is_authenticated}")

# Retrieve user profile
    user_profile = user_data.get_demographics("user123")
    print(f"User profile: {user_profile}")

# Add user and AI messages to the cache
    user_data.add_cache(user_id="user123", message_type="user", message="How are you?")
    user_data.add_cache(user_id="user123", message_type="ai", message="I'm doing well, thank you!")

# Retrieve session data (cache)
    user_cache = user_data.get_cache("user123")
    print(f"User session data: {user_cache}")

    reponse = api_usage.ask_ai(user_input="im upset", user_id="user123", user_data=user_data)
    print(f"User session data: {user_cache}")
