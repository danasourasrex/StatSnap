import os
from flask import Flask, flash, render_template,request, redirect, url_for, session
from werkzeug.utils import secure_filename
from database.UserDAO import UserDAO
from database.User import User
from database.ChatDBtoOracle import ChatDBtoOracle
from database.SQLStatCommandsDAO import SQLStatCommandsDAO
from database.StatIdDAO import StatIdDAO
from database.StatLookUpDAO import StatLookUpDAO
from database.ExpandedDataDAO import ExpandedDataDAO
from database.HandleDAO import HandleDAO
from database.Handle import Handle
from database.MessageDAO import MessageDAO
from database.StatIdStatLookUpExpandedDataDAO import StatIdStatLookUpExpandedDataDAO
from database.StatLookup import StatLookup


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
    handle_dao=HandleDAO()
    list_of_handle_ids=handle_dao.select_distinct_handle_ids(dao.username)

    for handle in list_of_handle_ids:
        dao.insert_avg_message_length_by_handle(handle)
        dao.insert_avg_message_length_by_handle_is_from_me(handle,0)
        dao.insert_avg_message_length_by_handle_is_from_me(handle,1)
        dao.insert_longest_message_length_by_handle(handle)
        dao.insert_longest_message_length_by_handle_is_from_me(handle,0)
        dao.insert_longest_message_length_by_handle_is_from_me(handle,1)
        dao.insert__minimum_length_message_by_handle(handle)
        dao.insert__minimum_length_message_by_handle_is_from_me(handle,0)
        dao.insert__minimum_length_message_by_handle_is_from_me(handle,1)
        dao.insert_total_text_messages_by_handle(handle)
        dao.insert_total_text_messages_by_handle_is_from_me(handle,0)
        dao.insert_total_text_messages_by_handle_is_from_me(handle,1)
        dao.insert_date_of_first_text_by_handle(handle)
        dao.insert_date_of_first_text_by_handle_is_from_me(handle,0)
        dao.insert_date_of_first_text_by_handle_is_from_me(handle,1)
        dao.insert_profane_language_count_by_handle(handle)
        dao.insert_profane_language_count_by_handle_is_from_me(handle,0)
        dao.insert_profane_language_count_by_handle_is_from_me(handle,1)
        dao.insert_most_common_word_by_handle(handle)
        dao.insert_most_common_word_by_handle_is_from_me(handle,0)
        dao.insert_most_common_word_by_handle_is_from_me(handle,1)
        dao.insert_day_with_most_texts_by_handle(handle)
        dao.insert_texts_over_time_by_handle(handle)
    dao.batch_commit_stat_expanded()


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method=='POST':
        return "hi MIKE"
    elif request.method=='GET':
        list_of_messages = get_all_user_messages(str(session['username']))
        return render_template('index.html',**locals())


def get_data_from_stats(list_of_stats):
    list_of_data_obj=[]
    stat_look_up=StatLookUpDAO()
    for stat in list_of_stats:
        stat_look_up_obj=stat_look_up.select(stat.get_stat_id())
        if stat_look_up_obj.get_data() is None:
            list_of_occurences =get_list_of_occurences(stat.get_stat_id())
            list_of_data_obj.append(list_of_occurences)
        else:
            list_of_data_obj.append(stat_look_up.select(stat.get_stat_id()))

    return list_of_data_obj


def get_list_of_occurences(stat_id):
    expanded_data_dao=ExpandedDataDAO()
    list_of_expanded_data=expanded_data_dao.select(stat_id)
    return list_of_expanded_data


def get_all_user_messages(user_id):
    message_dao = MessageDAO()
    return message_dao.select_all_users_messages(user_id)


def get_stat_id(handle_id):
    stat_id_dao = StatIdDAO()
    list_of_stat_id = stat_id_dao.select_all(handle_id)
    return list_of_stat_id


@app.route('/upload_file', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if isValid(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            if not get_stat_id(session['username']):
                return redirect(url_for('upload_file'))
            else:
                return redirect(url_for('general_charts'))

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


@app.route('/handle_charts', methods=['GET','POST'])
def handle_charts(handle=0):
    if request.method == 'POST':
        handle = request.form['handles']
    else:
        handle = 1
    # for testing
    # session['username'] = 'dsmolinski'

    # get data from DAOS
    stats_dao = StatIdStatLookUpExpandedDataDAO()
    list_of_stats = stats_dao.return_expanded_data_stats(str(session['username']))
    list_of_other_stats = stats_dao.return_all_none_stats(str(session['username']))
    handle_dao = HandleDAO()
    handles_and_nums = handle_dao.select_all_distinct_handles_for_user(str(session['username']))

    phone_num = ''
    for nums in handles_and_nums:
        if int(nums[0]) == int(handle):
            phone_num = nums[1]
            break

    # get distinct handles
    unique_handles = list()
    for x in range(len(list_of_stats)):
        found = False
        for handle2 in unique_handles:
            if handle2 == list_of_stats[x][2]:
                found = True
        if not found:
            unique_handles.append(list_of_stats[x][2])
    unique_handles.remove('9999999999999')
    for x in range(len(unique_handles)):
        unique_handles[x] = int(unique_handles[x])
    unique_handles.sort()
    for x in range(len(unique_handles)):
        unique_handles[x] = str(unique_handles[x])
    print(unique_handles)
    num_handles = len(unique_handles)


    list_of_stats_filtered = list()
    list_of_other_stats_filtered = list()
    for x in range(len(list_of_stats)):
        if list_of_stats[x][2] == str(handle):
            list_of_stats_filtered.append(list_of_stats[x])
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][2] == str(handle):
            list_of_other_stats_filtered.append(list_of_other_stats[x])

    # Texts over time setup
    texts_over_time = list()
    for x in range(len(list_of_stats_filtered)):
        if list_of_stats_filtered[x][3] == 'Texts Over Time - Handle':
            texts_over_time.append([list_of_stats_filtered[x][4], list_of_stats_filtered[x][5]])
    num_datapoints_tot = len(texts_over_time)

    fav_words_not_from_me_labels = list()
    fav_words_not_from_me_data = list()
    fav_words_from_me_labels = list()
    fav_words_from_me_data = list()
    for x in range(len(list_of_stats_filtered)):
        if list_of_stats_filtered[x][3] == '5 Most Used Words and Associated Occurrences - Handle':
            fav_words_not_from_me_labels.append(list_of_stats_filtered[x][4])
            fav_words_not_from_me_data.append(list_of_stats_filtered[x][5])
        if list_of_stats_filtered[x][3] == '5 Most Used Words and Associated Occurrences - Handle Not From Me':
            fav_words_from_me_labels.append(list_of_stats_filtered[x][4])
            fav_words_from_me_data.append(list_of_stats_filtered[x][5])

    # profane language
    total_profane_lang = 0
    profane_sent = 0
    profane_rec = 0
    for x in range(len(list_of_other_stats_filtered)):
        if list_of_other_stats_filtered[x][4] == 'Total Occurrences of Profane Language - Handle':
            total_profane_lang = int(list_of_other_stats_filtered[x][5])
        if list_of_other_stats_filtered[x][4] == 'Total Occurrences of Profane Language - Handle Not From Me':
            profane_rec = int(list_of_other_stats_filtered[x][5])
        if list_of_other_stats_filtered[x][4] == 'Total Occurrences of Profane Language - Handle From Me':
            profane_sent = int(list_of_other_stats_filtered[x][5])

    average_message_length_general = 0
    total_messages_general = 0
    date_of_first_text = ''
    for x in range(len(list_of_other_stats_filtered)):
        if list_of_other_stats_filtered[x][4] == 'Average Message Length - Handle':
            average_message_length_general = int(list_of_other_stats_filtered[x][5])
        if list_of_other_stats_filtered[x][4] == 'Total Texts - Handle':
            total_messages_general = int(list_of_other_stats_filtered[x][5])
        if list_of_other_stats_filtered[x][4] == 'Date of First Text - Handle':
            date_of_first_text = str(list_of_other_stats_filtered[x][5])

    # longest/Shortest Message received
        shortest_message = ''
        longest_message = ''
        for x in range(len(list_of_other_stats_filtered)):
            if list_of_other_stats_filtered[x][4] == 'Shortest Message - Handle':
                shortest_message = str(list_of_other_stats_filtered[x][5])
            if list_of_other_stats_filtered[x][4] == 'Longest Message - Handle':
                longest_message = str(list_of_other_stats_filtered[x][5])

    return render_template('handle_charts.html', **locals())


@app.route('/general_charts', methods=['GET', 'POST'])
def general_charts():
    # for testing
    # session['username'] = 'dsmolinski'
    stats_dao = StatIdStatLookUpExpandedDataDAO()
    list_of_stats = stats_dao.return_expanded_data_stats(str(session['username']))

    list_of_other_stats = stats_dao.return_all_none_stats(str(session['username']))

    # this is hands down the worst unmaintainable hardcoded garbage code I have ever written lmao
    # favorite words not from me

    fav_words_not_from_me_labels = list()
    fav_words_not_from_me_data = list()
    fav_words_from_me_labels = list()
    fav_words_from_me_data = list()
    for x in range(len(list_of_stats)):
        if list_of_stats[x][3] == '5 Most Used Words and Associated Occurrences - General Not From Me':
            fav_words_not_from_me_labels.append(list_of_stats[x][4])
            fav_words_not_from_me_data.append(list_of_stats[x][5])
        if list_of_stats[x][3] == '5 Most Used Words and Associated Occurrences - General From Me':
            fav_words_from_me_labels.append(list_of_stats[x][4])
            fav_words_from_me_data.append(list_of_stats[x][5])

    average_message_length_general = 0
    total_messages_general = 0
    unique_numbers = 0
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][4] == 'Average Message Length - General':
            average_message_length_general = int(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Total Texts - General':
            total_messages_general = int(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Unique Numbers - General':
            unique_numbers = int(list_of_other_stats[x][5])

    # Texts over time setup
    texts_over_time = list()
    texts_over_time_rec = list()
    texts_over_time_sent = list()
    for x in range(len(list_of_stats)):
        if list_of_stats[x][3] == 'Texts Over Time - General':
            texts_over_time.append([list_of_stats[x][4], list_of_stats[x][5]])
        if list_of_stats[x][3] == 'Texts Over Time - General Not From Me':
            texts_over_time_rec.append([list_of_stats[x][4], list_of_stats[x][5]])
        if list_of_stats[x][3] == 'Texts Over Time - General From Me':
            texts_over_time_sent.append([list_of_stats[x][4], list_of_stats[x][5]])
    num_datapoints_tot = len(texts_over_time)
    num_datapoints_sent = len(texts_over_time_sent)
    num_datapoints_rec = len(texts_over_time_rec)

    # days with most text
    day_with_most_texts_general = 0
    day_with_most_texts_general_number = 0
    day_with_most_texts_rec = 0
    day_with_most_texts_rec_number = 0
    day_with_most_texts_sent = 0
    day_with_most_texts_sent_number = 0
    for x in range(len(list_of_stats)):
        if list_of_stats[x][3] == 'Day With Most Texts - General':
            day_with_most_texts_general = list_of_stats[x][4]
            day_with_most_texts_general_number = list_of_stats[x][5]
        if list_of_stats[x][3] == 'Day With Most Texts - General Not From Me':
            day_with_most_texts_rec = list_of_stats[x][4]
            day_with_most_texts_rec_number = list_of_stats[x][5]
        if list_of_stats[x][3] == 'Day With Most Texts - General From Me':
            day_with_most_texts_sent = list_of_stats[x][4]
            day_with_most_texts_sent_number = list_of_stats[x][5]

    # profane language
    total_profane_lang = 0
    profane_sent = 0
    profane_rec = 0
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][4] == 'Total Occurrences of Profane Language - General':
            total_profane_lang = int(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Total Occurrences of Profane Language - General Not From Me':
            profane_rec = int(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Total Occurrences of Profane Language - General From Me':
            profane_sent = int(list_of_other_stats[x][5])

    # most frequently spoken to
    most_freq_spoken_general = 'Not Found'
    most_freq_spoken_from = 'Not Found'
    most_freq_spoken_to = 'Not Found'
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][4] == 'Most Frequently Spoken To - General':
            most_freq_spoken_general = str(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Most Messages From - General':
            most_freq_spoken_from = str(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Most Messages To - General':
            most_freq_spoken_to = str(list_of_other_stats[x][5])

    # sent vs received
    messages_sent_general = 0
    messages_received_general = 0
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][4] == 'Total Texts - General Not From Me':
            messages_received_general = str(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Total Texts - General From Me':
            messages_sent_general = str(list_of_other_stats[x][5])

    # longest/Shortest Message received
    shortest_message = ''
    longest_message = ''
    for x in range(len(list_of_other_stats)):
        if list_of_other_stats[x][4] == 'Shortest Message - General':
            shortest_message = str(list_of_other_stats[x][5])
        if list_of_other_stats[x][4] == 'Longest Message - General':
            longest_message = str(list_of_other_stats[x][5])

    return render_template("charts.html", **locals())


@app.route('/faq', methods=['GET'])
def faq():
    return render_template("faq.html")


def isValid(username,password):
    userDao = UserDAO()
    if not userDao.select(username):
        return False
    return userDao.select(username).get_password() == password




if __name__ == "__main__":
    app.run()
    #app.run(host='0.0.0.0', port=5000)
