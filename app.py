from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from LPI import interpolator, csv_to_array, get_var
import requests
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def live():
    return 'active'

@app.route('/upload-csv')
def upload_file():
    return render_template("upload-csv.html")


@app.route('/output', methods=['POST', 'PATCH'])
def output():
    
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            print('no file selected')
            return render_template('upload-csv.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            print('no file selected')
            return render_template('upload-csv.html', msg='No file selected')
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

            # text input:
            var = request.form['text']

            X, Y = csv_to_array(f'uploads/{file.filename}')
            var = get_var(var)
            poly = interpolator(var, X, Y)
            result = poly.calc()
            latex_eq, latex_var = poly.reformat(result, 2)
            poly.plotter(result, latex_eq, latex_var)

    return render_template("output.html", msg='select a csv and variable name')


if __name__ == '__main__':
    app.run()
