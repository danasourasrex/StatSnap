import os
from flask import Flask, flash, render_template,request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3
import cx_Oracle
import emoji

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

    connection = sqlite3.connect("db_upload/chat.db")
    cursor = connection.cursor()
    cursor.execute("select text, handle_id, is_from_me, date from message")
    acceptable_messages = []


    i = 0
    for rows in cursor.fetchall():
        if i == 120:
            break
        elif str(rows[1]) != "32" and "quiz" not in str(rows[0]) and "algorithms" not in str(rows[0]):
            i += 1
            acceptable_messages.append([str(rows[0]),str(rows[1]),str(rows[2]), str(rows[3])])

    for rows in acceptable_messages:
        print(rows)

    ip = 'stonehillcsc325.cjjvanphib99.us-west-2.rds.amazonaws.com'
    port = 1521
    SID = 'ORCL'
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)
    con = cx_Oracle.connect('mwojtyna', 'csrocks55', dsn_tns)
    cur = con.cursor()
    for rows in acceptable_messages:
        command_string = "insert into MESSAGE(HANDLE_ID, TEXT_MESSAGE, IS_FROM_ME, DATE_OF_TEXT) values ("\
        ":1,:2,:3,:4 )"
        cur.execute(command_string, (str(rows[1]), deEmojify(str(rows[0])), str(rows[2]), str(rows[3])))
    con.commit()

    cursor.execute("select ROWID, id, service from handle")
    handle_rows = []
    for rows in cursor.fetchall():
        handle_rows.append([str(rows[0]),str(rows[1]),str(rows[2])])



    for rows in handle_rows:
        command_string = "insert into HANDLE(HANDLE_ID, PHONE_NUMBER, SERVICE) values ("\
        ":1,:2,:3)"
        cur.execute(command_string, (str(rows[0]), str(rows[1]), str(rows[2])))
    con.commit()

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
    return render_template("login.html")

@app.route('/create_account', methods = ['GET', 'POST'])
def create_account():
    return render_template("create_account.html")




if __name__ == "__main__":
    app.run()