from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'static/files/'
ALLOWED_EXTENSIONS = {'json', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '78828077bdd7a66c88ac6d2ede4d8bfb72e5031b6234dc8f9e63e67a6d55713c'

def is_allowed(filename):
    extension = filename.rsplit('.', 1)[1]
    return '.' in filename and extension in ALLOWED_EXTENSIONS, extension

def export(data):
         return render_template('result.html', data=data)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file detected")
            return redirect(request.url)

        f = request.files['file']
        if f and is_allowed(f.filename)[0]:
            filename = secure_filename(f.filename)
            print(is_allowed(f.filename)[1])
            file_location = os.path.join(UPLOAD_FOLDER, filename)
            f.save(file_location)
            if is_allowed(f.filename)[1] == 'csv':
                data = pd.read_csv(file_location)

            if is_allowed(f.filename)[1] == 'json':
                data = pd.read_json(file_location)
            df = pd.DataFrame(data, columns=['names', 'points'])
            df.sort_values(by=['points'], inplace=True, ascending=False)
            print(df.values[:6])
            print(df.head())
            # return render_template('index.html', data=data)
            return render_template("result.html", data=df.values, total=len(df))
        else:
            flash("Please select a csv or json file")
            return redirect(url_for('home'))
    return render_template('upload.html')



@app.route('/leaderboard')
def leaderboard():
    return render_template('index.html')

@app.route('/result')
def result():
         return render_template('result.html', data=[])

if __name__ == '__main__':
    app.run(debug=True)