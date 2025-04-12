from flask import Flask, render_template, request
from backend import api_usage

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/get',methods=['GET'])
def get():
    return api_usage.ask_ai(request.args.get("msg"))

if __name__ == "__main__":
    app.run()
