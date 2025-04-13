from flask import Flask, render_template, request,redirect, url_for
from backend import api_usage
from backend import db_formation
import os

app = Flask(__name__)
db = db_formation.UserData(os.getenv('PG_URI'))
db.create_tables()

@app.route('/')
def main():
   return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
   if request.method != 'POST':
    return render_template('login.html')
   user = request.form.get("username")
   password = request.form.get("password")
   if not db.check_user(user,password):
    return render_template('login.html')
   return render_template("index.html", username=user)
   
@app.route('/register', methods=['POST'])
def register():
   db.add_demographics(request.form.get('username'), request.form.get('password'))
   return render_template("login.html")

@app.route('/chat',methods=['POST','GET'])
def chat():
    return render_template('index.html', request.args.get('user'))

@app.route('/get')
def get():
   return api_usage.ask_ai(request.args.get('msg'),request.args.get('user'), db)

@app.route('/edit-profile',methods=['POST','GET'])
def editProfile():
    if request.method == 'POST':
        db.update_demographics(request.form.get('user'),request.form.get('name'),request.form.get('age') if request.form.get('age') else 0,
                            request.form.get('gender'),request.form.get('location'),request.form.get('occupation'),
                            request.form.get('expectations'))
        return render_template('index.html', username=request.form.get('user'))
    return render_template('edit-profile.html', user = request.args.get('user'))


@app.route('/greet',methods=['GET'])
def greet():
    return api_usage.greet()

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == "__main__":
    app.run()
