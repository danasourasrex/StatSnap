from database.DAO import DAO
import time
from better_profanity import profanity
from collections import Counter
from database.StatId import StatId
from database.StatIdDAO import StatIdDAO
from database.StatLookup import StatLookup
from database.StatLookUpDAO import StatLookUpDAO

class SQLStatCommandsDAO(DAO):
    def __init__(self, username):
        DAO.__init__(self)
        self.username = username
        self.insert_avg_message_length_general()
        self.insert_longest_length_text_message_general()
        self.insert_minimum_length_text_message_general()
        self.insert_total_text_messages_general()
        self.insert_unique_numbers_general()
        self.insert_date_of_first_text_general()
        self.insert_profane_language_count_general()
        self.insert_most_common_word_general()
        self.insert_day_with_most_texts_general()
        self.insert_most_frequently_spoken_to_general()
        self.insert_most_messages_from_general()
        self.insert_most_messages_to_general()

    def generate_data_insert(self, stat_id, handle_id, stat_name, data):
        stat_id_obj = StatId()
        stat_id_obj.set_values_from_row([self.username, str(stat_id), str(handle_id)])
        stat_look_up = StatLookup()
        stat_look_up.set_values_from_row(
            [self.username, str(stat_id), str(stat_name), str(data), str(handle_id)])
        stat_id_dao = StatIdDAO()
        stat_look_up_dao = StatLookUpDAO()
        stat_id_dao.insert(stat_id_obj)
        stat_look_up_dao.insert(stat_look_up)


    def insert_avg_message_length_general(self):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE"
        self.cur.execute(command_string)
        self.generate_data_insert(1, 99999999, "Average Message Length - General", str(self.cur.fetchone()[0]))

    def insert_longest_length_text_message_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        self.cur.execute(command_string)
        self.generate_data_insert(2, 99999999, "Longest Message - General", str(self.cur.fetchone()[0]))

    def insert_minimum_length_text_message_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        self.cur.execute(command_string)
        self.generate_data_insert(3, 99999999, "Shortest Message - General", str(self.cur.fetchone()[0]))

    def insert_total_text_messages_general(self):
        command_string = "SELECT COUNT(*) FROM MESSAGE"
        self.cur.execute(command_string)
        self.generate_data_insert(4, 99999999, "Total Texts - General", str(self.cur.fetchone()[0]))

    def insert_unique_numbers_general(self):
        command_string = "SELECT COUNT(DISTINCT(HANDLE_ID)) FROM MESSAGE"
        self.cur.execute(command_string)
        self.generate_data_insert(5, 99999999, "Unique Numbers - General", str(self.cur.fetchone()[0]))

    def insert_date_of_first_text_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE)"
        self.cur.execute(command_string)
        self.generate_data_insert(6, 99999999, "Date of First Text - General", str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((self.cur.fetchone()[0] / 1000000000) + 978307200)))))

    def insert_profane_language_count_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        self.cur.execute(command_string)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        self.generate_data_insert(7, 99999999, "Total Occurences of Profane Language  - General", str(profane_language_count))

    def insert_most_common_word_general(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        self.cur.execute(command_string)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        self.generate_data_insert(8, 99999999, "5 Most Used Words and Associated Occurences  - General", str(counter.most_common(5)))

    def insert_day_with_most_texts_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE"
        self.cur.execute(command_string)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        self.generate_data_insert(9, 99999999, "Day With Most Texts  - General", str(counter.most_common(1)))

    def insert_texts_over_time_general(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE ORDER BY DATE_OF_TEXT ASC"
        self.cur.execute(command_string)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        print(counter)

    def insert_most_frequently_spoken_to_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        self.generate_data_insert(10, 99999999, "Most Frequently Spoken To - General", str(self.cur.fetchone()[0]))


    def insert_most_messages_from_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        self.generate_data_insert(11, 99999999, "Most Messages From - General", str(self.cur.fetchone()[0]))

    def insert_most_messages_to_general(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        self.generate_data_insert(12, 99999999, "Most Messages To - General", str(self.cur.fetchone()[0]))












