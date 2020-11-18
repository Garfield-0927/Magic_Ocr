from flask import Flask,render_template, request, jsonify, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/show')
def show():
    return render_template('show.html')


if __name__ == '__main__':
    app.run()
