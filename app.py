from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import requests
import json
import cv2
import base64
import os


def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tostring()).decode('utf8')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = True
app.jinja_env.auto_reload = True


@app.route('/')
def hello_world():
    return redirect('/index')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/show', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        file = request.files['file']
        # print(request.form)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print('success')
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # print(img_path)
            # terminal 里输入 hub serving start -m chinese_ocr_db_crnn_mobile -p 8866
            data = {'images': [cv2_to_base64(cv2.imread(img_path))]}
            headers = {"Content-type": "application/json"}
            url = "http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_mobile"
            r = requests.post(url=url, headers=headers, data=json.dumps(data))
            results = (r.json()["results"])
            # print(results[0])

            res = []
            for item in results[0]['data']:
                res.append(item['text'])

            # print(res)
            return render_template('show.html', img_path=img_path, res=res)
    return render_template('show.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8899, debug=True)
