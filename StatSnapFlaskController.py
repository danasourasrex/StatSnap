import os
from flask import Flask, flash, render_template,request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = './db_upload'
ALLOWED_EXTENSIONS = set(['db', 'png'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/database_view/')
def uploaded_file():
    connection = sqlite3.connect("db_upload/chat.db")
    cursor = connection.cursor()
    cursor.execute("select id, text from message, handle where message.handle_id = handle.ROWID;")
    results = cursor.fetchall()
    return render_template("database_view.html", results = results)

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    msg = 'Please select a valid file.'
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        if 'file' not in request.files:
            flash(msg)
            return render_template("index.html")
        file = request.files['file']
        if file.filename == '':
            flash(msg)
            return render_template("index.html")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file'))
        else:
            flash(msg)




if __name__ == "__main__":
    app.run()