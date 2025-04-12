from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/get',methods=['GET'])
def main():
    return render_template('get.html')
