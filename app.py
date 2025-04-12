from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/get',methods=['GET'])
def get():
    return "hello"

if __name__ == "__main__":
    app.run()
