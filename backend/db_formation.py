from dotenv import load_dotenv
import os
import psycopg
from psycopg import sql

load_dotenv()

conn_url = os.getenv("PG_URI")

class UserData:

    def __init__(self, conn_url):
        self.conn = psycopg.connect(conn_url)
        self.cursor = self.conn.cursor()

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
            session_data TEXT
            );
        """)
    
        self.conn.commit()
    
    def add_demographics(self, user_id: str, password: str, name: str, age: int, gender: str, location: str = None, occupation: str = None):
        self.cur.execute("""
            INSERT INTO demographics (user_id, password, name, age, gender, location, occupation)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (user_id) 
            DO UPDATE SET
                name = EXCLUDED.name, age = EXCLUDED.age, gender = EXCLUDED.gender,
                location = EXCLUDED.location, occupation = EXCLUDED.occupation;
        """, (user_id, name, age, gender, location, occupation))
        
        self.conn.commit()

    def add_cache(self, user_id: str, message: str):
        self.cur.execute("""
            INSERT INTO cache (user_id, message)
            VALUES (%s, %s);
        """, (user_id, message))
        
        self.conn.commit()

    def get_demographics(self, user_id):
        self.cursor.execute("""
            SELECT user_id, name, age, gender, location, occupation, expectations
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
            SELECT session_data FROM cache WHERE user_id = %s;
        """, (user_id,))
        
        sessions = self.cursor.fetchall()

        if sessions:
            return sessions
        else:
            return "No sessions found for this user."
        
    def check_user(self, user_id, password):
        self.cursor.execute("""
            SELECT password FROM demographics WHERE user_id = %s AND password = %s;
        """, (user_id, password))

        stored_password = self.cursor.fetchone()

        return bool(stored_password)
