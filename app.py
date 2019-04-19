from flask import Flask, render_template,request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/open', methods=['POST', 'GET'])
def open():
    return render_template('index.html')

@app.route('/close', methods=['POST', 'GET'])
def close():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
