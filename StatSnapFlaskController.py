import os
from flask import Flask, flash, render_template,request, redirect, url_for, session
from werkzeug.utils import secure_filename
import sqlite3
import cx_Oracle
from database.UserDAO import UserDAO
from database.User import User


UPLOAD_FOLDER = './db_upload'
ALLOWED_EXTENSIONS = set(['db'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/database_view/')
def uploaded_file():



    return render_template("database_view.html")

@app.route('/upload_file', methods = ['GET', 'POST'])
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
            return render_template("index.html")

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if isValid(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('upload_file'))


    return render_template("login.html")

@app.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        userDao = UserDAO()
        user = User()
        user.set_values_from_row([str(request.form['username']), str(request.form['password'])])
        userDao.insert(user)
        return redirect(url_for('login'))

    return render_template("create_account.html")


def isValid(username,password):
    userDao = UserDAO()
    if not userDao.select(username):
        return False
    return userDao.select(username).get_password() == password




if __name__ == "__main__":
    app.run()