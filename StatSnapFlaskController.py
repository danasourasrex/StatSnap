import os
from flask import Flask, flash, render_template,request, redirect, url_for, session
from werkzeug.utils import secure_filename
from database.UserDAO import UserDAO
from database.User import User
from database.ChatDBtoOracle import ChatDBtoOracle
from database.SQLStatCommandsDAO import SQLStatCommandsDAO
from database.StatIdDAO import StatIdDAO
from database.StatLookUpDAO import StatLookUpDAO



UPLOAD_FOLDER = './db_upload'
ALLOWED_EXTENSIONS = set(['db'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_data(dao):
    dao.insert_avg_message_length_general()
    dao.insert_avg_message_length_general_is_from_me(0)
    dao.insert_avg_message_length_general_is_from_me(1)

    dao.insert_longest_length_text_message_general()
    dao.insert_longest_length_text_message_general_is_from_me(0)
    dao.insert_longest_length_text_message_general_is_from_me(1)

    dao.insert_minimum_length_text_message_general()
    dao.insert_minimum_length_text_message_general_is_from_me(0)
    dao.insert_minimum_length_text_message_general_is_from_me(1)

    dao.insert_total_text_messages_general()
    dao.insert_total_text_messages_general_is_from_me(0)
    dao.insert_total_text_messages_general_is_from_me(1)

    dao.insert_unique_numbers_general()
    dao.insert_date_of_first_text_general()
    dao.insert_date_of_first_text_general_is_from_me(0)
    dao.insert_date_of_first_text_general_is_from_me(1)

    dao.insert_profane_language_count_general()
    dao.insert_profane_language_count_general_is_from_me(0)
    dao.insert_profane_language_count_general_is_from_me(1)

    dao.insert_most_common_word_general()
    dao.insert_most_common_word_general_is_from_me(0)
    dao.insert_most_common_word_general_is_from_me(1)

    dao.insert_day_with_most_texts_general()
    dao.insert_day_with_most_texts_general_is_from_me(0)
    dao.insert_day_with_most_texts_general_is_from_me(1)

    dao.insert_texts_over_time_general()
    dao.insert_texts_over_time_general_is_from_me(0)
    dao.insert_texts_over_time_general_is_from_me(1)
    dao.insert_most_frequently_spoken_to_general()
    dao.insert_most_messages_from_general()
    dao.insert_most_messages_to_general()

    #dao.insert_avg_message_length_by_handle()
    #dao.insert_avg_message_length_by_handle_is_from_me()
    #dao.insert_longest_message_length_by_handle()
    #dao.insert_longest_message_length_by_handle_is_from_me(0)
    #dao.insert_longest_message_length_by_handle_is_from_me(1)
    #dao.insert__minimum_length_message_by_handle(self, handle_id)
    #dao.insert__minimum_length_message_by_handle_is_from_me(0)
    #dao.insert__minimum_length_message_by_handle_is_from_me(1)
    #dao.insert_total_text_messages_by_handle()
    # dao.insert_total_text_messages_by_handle_is_from_me(0)
    # dao.insert_total_text_messages_by_handle_is_from_me(1)
    # dao.insert_date_of_first_text_by_handle()
    # dao.insert_date_of_first_text_by_handle_is_from_me(0)
    #dao.insert_date_of_first_text_by_handle_is_from_me(1)
    #dao.insert_profane_language_count_by_handle
    #dao.insert_profane_language_count_by_handle_is_from_me
    #dao.insert_profane_language_count_by_handle_is_from_me
    # dao.insert_most_common_word_by_handle()
    # dao.insert_most_common_word_by_handle_is_from_me(0)
    # dao.insert_most_common_word_by_handle_is_from_me(1)
    #dao.insert_day_with_most_texts_by_handle()


@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method=='POST':
        return "hi MIKE"
    elif request.method=='GET':
        list_of_stats=get_stat_id(session['username'])
        return list_of_stats

def get_stat_id(handle_id):
    stat_id_dao = StatIdDAO()
    list_of_stat_id = stat_id_dao.select_all(handle_id)
    return list_of_stat_id

@app.route('/upload_file', methods = ['GET', 'POST'])
def upload_file():
    msg = 'Please select a valid file.'
    if request.method == 'GET':
        return render_template("UploadFile.html",**locals())
    elif request.method == 'POST':
        if 'file' not in request.files:
            flash(msg)
            return render_template("UploadFile.html",**locals())
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            chat_db_to_oracle = ChatDBtoOracle()
            chat_db_to_oracle.add_messages_to_db(str(session['username']))
            chat_db_to_oracle.add_handles_to_db(str(session['username']))
            sql_stat_commands_dao = SQLStatCommandsDAO(str(session['username']))
            generate_data(sql_stat_commands_dao)
            return redirect(url_for('index'))
        else:
            flash(msg)
            return render_template("UploadFile.html",**locals())

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if isValid(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            has_uploaded = get_stat_id(session['username']) == None
            if not has_uploaded:
                return redirect(url_for('upload_file'))
            else:
                return redirect(url_for('index'))


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