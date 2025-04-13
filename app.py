from flask import Flask, render_template, request,redirect, url_for
from backend import api_usage
from backend import db_formation
from dotenv import load_dotenv

app = Flask(__name__)
db = db_formation(load_dotenv('PG_URI'))
db.create_tables()

@app.route('/')
def main():
   return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
   user = request.form.get("username")
   password = request.form.get("password")
   if not db.check_user(user,password):
    return render_template('login.html')
   return render_template("index.html")
   

@app.route('/chat',methods=['POST','GET'])
def chat():
    return render_template('index.html')

@app.route('/get')
def get():
   return api_usage.ask_ai(request.args.get('msg'),request.args.get('user'), db)

@app.route('/edit-profile',methods=['POST','GET'])
def editProfile():
    if request.method == 'GET':
        return render_template('edit-profile.html')
    return redirect("/chat")

@app.route('/register', methods =['POST'])
def register():
   user = request.form.get("username")
   password = request.form.get("password")
   db.add_demographics(user,password)
   return render_template('login.html')

@app.route('/greet',methods=['GET'])
def greet():
    return api_usage.greet()

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()
