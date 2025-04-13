from flask import Flask, render_template, request,redirect, url_for
from backend import api_usage

app = Flask(__name__)

@app.route('/')
def main():
   return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def login():
   user = request.form.get("username")
   password = request.form.get("password")
   if (not user or not password):
    return render_template('login.html')
   return render_template("index.html")
   

@app.route('/chat')
def chat():
    return render_template('index.html')

@app.route('/get')
def get():
   return api_usage.ask_ai(request.args.get('msg'))

@app.route('/edit-profile')
def editProfile():
    return render_template('edit-profile.html')


@app.route('/greet',methods=['GET'])
def greet():
    return api_usage.greet()

@app.route('/signup')
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    app.run()
