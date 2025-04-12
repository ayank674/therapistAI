from flask import Flask, render_template, request
from backend import api_usage

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/get',methods=['GET'])
def get():
    return api_usage.ask_ai(request.args.get("msg"))

@app.route('/greet',methods=['GET'])
def greet():
    return api_usage.greet()

@app.route('/edit-profile')
def edit():
    return render_template('edit-profile.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
if __name__ == "__main__":
    app.run()
