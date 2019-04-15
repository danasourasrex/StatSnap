from database.DAO import DAO
import time
from better_profanity import profanity
from collections import Counter
from database.StatId import StatId
from database.StatIdDAO import StatIdDAO
from database.StatLookup import StatLookup
from database.StatLookUpDAO import StatLookUpDAO
import cx_Oracle

class SQLStatCommandsDAO(DAO):
    is_from_me_arr={"Not from me","Is from me"}
    def __init__(self, username):
        DAO.__init__(self)
        self.username = username

    def generate_data_insert(self, stat_id,  stat_name, data):


        stat_look_up = StatLookup()
        stat_look_up.set_values_from_row(
            [str(stat_id), str(stat_name), str(data)])
        stat_id_dao = StatIdDAO()
        stat_look_up_dao = StatLookUpDAO()
        stat_id_obj = StatId()
        id=stat_look_up_dao.insert(stat_look_up)
        stat_id_obj.set_id(id)
        stat_id_obj.set_handle_id(self.username)
        stat_id_obj.set_stat_id(str(stat_id))
        stat_id_dao.insert(stat_id_obj)


    def insert_avg_message_length_general(self):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(1,  "Average Message Length - General", str(self.cur.fetchone()[0]))

    def insert_avg_message_length_general_is_from_me(self, is_from_me):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(12,"Average Message Length From Me",str(self.cur.fetchone()[0]))

    def insert_longest_length_text_message_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(2,  "Longest Message - General", str(self.cur.fetchone()[0]))

    def insert_longest_length_text_message_general_is_from_me(self, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE IS_FROM_ME = " + str(is_from_me) +")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(13,"Longest Message - General",self.cur.fetchone()[0])

    def insert_minimum_length_text_message_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(3,  "Shortest Message - General", str(self.cur.fetchone()[0]))

    def insert_minimum_length_text_message_general_is_from_me(self, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE IS_FROM_ME = " + str(is_from_me) +")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(14,"Shortest Message - Is From Me",self.cur.fetchone()[0])

    def insert_total_text_messages_general(self):
        command_string = "SELECT COUNT(*) FROM MESSAGE"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(4,  "Total Texts - General", str(self.cur.fetchone()[0]))

    def insert_total_text_messages_general_is_from_me(self, is_from_me):
        command_string = "SELECT COUNT(*) FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        print(14,"Total Texts - Is from Me",self.cur.fetchone()[0])

    def insert_unique_numbers_general(self):
        command_string = "SELECT COUNT(DISTINCT(HANDLE_ID)) FROM MESSAGE"
        self.cur.execute(command_string)
        self.generate_data_insert(5,  "Unique Numbers - General", str(self.cur.fetchone()[0]))

    def insert_date_of_first_text_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE)"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(6,  "Date of First Text - General", str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((self.cur.fetchone()[0] / 1000000000) + 978307200)))))

    def insert_date_of_first_text_general_is_from_me(self, is_from_me):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE IS_FROM_ME = "+ str(is_from_me) +" AND DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE WHERE IS_FROM_ME = " + str(is_from_me) + ")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(15,"Date first sent text",self.cur.fetchone()[0])

    def insert_profane_language_count_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        self.generate_data_insert(7,  "Total Occurences of Profane Language  - General", str(profane_language_count))

    def insert_profane_language_count_general_is_from_me(self, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        self.generate_data_insert(15,'Total Occurences of profane language from me',profane_language_count)

    def insert_most_common_word_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        self.generate_data_insert(8,  "5 Most Used Words and Associated Occurences  - General", str(counter.most_common(5)))

    def insert_most_common_word_general_is_from_me(self, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        self.generate_data_insert(16,  "5 Most Used Words and Associated Occurences  - Sent",counter)

    def insert_day_with_most_texts_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(9,  "Day With Most Texts  - General", str(counter.most_common(1)))

    def insert_day_with_most_texts_general_is_from_me(self, is_from_me):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(17,  "Day With Most Texts  - Sent", counter)

    def insert_texts_over_time_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE ORDER BY DATE_OF_TEXT ASC"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(18,"Texts Over Time _ General",counter)

    def insert_texts_over_time_general_is_from_me(self, is_from_me):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE IS_FROM_ME = "+ str(is_from_me) +" ORDER BY DATE_OF_TEXT ASC"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(19,"Texts Over Time _ is From Me",(counter))

    def insert_most_frequently_spoken_to_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(10,  "Most Frequently Spoken To - General", str(self.cur.fetchone()[0]))

    def insert_most_messages_from_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(11,  "Most Messages From - General", str(self.cur.fetchone()[0]))

    def insert_most_messages_to_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(12,  "Most Messages To - General", str(self.cur.fetchone()[0]))

    def insert_avg_message_length_by_handle(self, handle_id):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id)
        self.cur.execute(command_string)
        self.generate_data_insert(20,"Average legth of messages",self.cur.fetchone()[0])

    def insert_avg_message_length_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(21,"Average legth of messages",self.cur.fetchone()[0])

    def insert_longest_message_length_by_handle(self, handle_id):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID =" + str(handle_id) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE HANDLE_ID = " + str(handle_id) +")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(22,"Insert Longest Message length by handleID -General" ,self.cur.fetchone()[0])

    def insert_longest_message_length_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID =" + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE HANDLE_ID = " + str(handle_id) +" AND IS_FROM_ME = " + str(is_from_me) + ")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.cur.execute(command_string)
        self.generate_data_insert(23,"Insert Longest Message length by handleID"+self.is_from_me_arr[is_from_me],self.cur.fetchone()[0])

    def insert__minimum_length_message_by_handle(self, handle_id):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID =" + str(handle_id) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE HANDLE_ID = " + str(handle_id) +")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(24,"Insert Minimum Message length by handle id",self.cur.fetchone()[0])

    def insert__minimum_length_message_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID =" + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me) + " AND LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE WHERE HANDLE_ID = " + str(handle_id) +" AND IS_FROM_ME = " + str(is_from_me) + ")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(25,"Insert Minimum Message length"+self.is_from_me_arr[is_from_me],self.cur.fetchone()[0])

    def insert_total_text_messages_by_handle(self, handle_id):
        command_string = "SELECT COUNT(*) FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(26,"Insert Total Messages- General",self.cur.fetchone()[0])


    def insert_total_text_messages_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT COUNT(*) FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(27,"Insert Total Messages-"+self.is_from_me_arr[is_from_me],self.cur.fetchone()[0])

    def insert_date_of_first_text_by_handle(self, handle_id):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE WHERE HANDLE_ID = " + str(handle_id) + ")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(28, "Insert Total Messages- General",(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((self.cur.fetchone()[0] / 1000000000) + 978307200))))))

    def insert_date_of_first_text_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me) + " AND DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me) + ")"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        self.generate_data_insert(29, "Insert Total Messages-"+self.is_from_me_arr[is_from_me],(str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((self.cur.fetchone()[0] / 1000000000) + 978307200))))))

    def insert_profane_language_count_by_handle(self, handle_id):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        self.generate_data_insert(30, "Insert Profane Language Count- General",str(profane_language_count))

    def insert_profane_language_count_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = " + str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        self.generate_data_insert(31, "Insert Profane Language Count"+self.is_from_me_arr[is_from_me],str(profane_language_count))

    def insert_most_common_word_by_handle(self, handle_id):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        self.generate_data_insert(32, "Insert Profane Language Count -General" ,str(counter.most_common(5)))

    def insert_most_common_word_by_handle_is_from_me(self, handle_id, is_from_me):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        self.generate_data_insert(33, "Insert Profane Language Count" + self.is_from_me_arr[is_from_me],str(counter.most_common(5)))

    def insert_day_with_most_texts_by_handle(self, handle_id):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id)
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(34, "Insert Day with most texts count-General",str(counter.most_common(1)))

    def insert_texts_over_time_by_handle(self,handle_id):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " ORDER BY DATE_OF_TEXT ASC"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(35, "Insert texts over time by handle",counter)

    def insert_texts_over_time_by_handle_is_from_me(self,handle_id, is_from_me):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE HANDLE_ID = " + str(handle_id) + " AND IS_FROM_ME = "+ str(is_from_me) + " ORDER BY DATE_OF_TEXT ASC"
        try:
            self.cur.execute(command_string)
        except cx_Oracle.DatabaseError as e:
            print(e)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(36, "Insert texts over time by handle", counter)







