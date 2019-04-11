from database.DAO import DAO
import time
from better_profanity import profanity
from collections import Counter

class SQLStatCommandsDAO(DAO):
    def __init__(self):
        DAO.__init__(self)


    def insert_avg_message_length(self):
        command_string = "SELECT ROUND(AVG((LENGTH(TEXT_MESSAGE)))) AS AVERGAE_MESSAGE_SIZE FROM MESSAGE"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_longest_length_text_message(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MAX(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_minimum_length_text_message(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE WHERE LENGTH(TEXT_MESSAGE) = (SELECT MIN(LENGTH(TEXT_MESSAGE))from MESSAGE)"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_total_text_messages(self):
        command_string = "SELECT COUNT(*) FROM MESSAGE"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_unique_numbers(self):
        command_string = "SELECT COUNT(DISTINCT(HANDLE_ID)) FROM MESSAGE"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_date_of_first_text(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE WHERE DATE_OF_TEXT = (SELECT MIN(DATE_OF_TEXT)from MESSAGE)"
        self.cur.execute(command_string)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int((self.cur.fetchone()[0] / 1000000000) + 978307200))))

    def insert_profane_language_count(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        self.cur.execute(command_string)
        profane_language_count = 0
        for rows in self.cur.fetchall():
            if profanity.contains_profanity(rows[0]) and rows[0] is not None:
                profane_language_count += 1
        print(profane_language_count)

    def insert_most_common_word(self):
        command_string = "SELECT TEXT_MESSAGE FROM MESSAGE"
        self.cur.execute(command_string)
        all_texts_as_string = ""
        for rows in self.cur.fetchall():
            all_texts_as_string += " " + str(rows[0]).lower()
        counter = Counter(all_texts_as_string.split())
        print(counter.most_common(20))

    def insert_day_with_most_texts(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE"
        self.cur.execute(command_string)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        print(counter.most_common(20))

    def insert_texts_over_time(self):
        command_string = "SELECT DATE_OF_TEXT FROM MESSAGE ORDER BY DATE_OF_TEXT ASC"
        self.cur.execute(command_string)
        all_dates_as_string = ""
        for rows in self.cur.fetchall():
            all_dates_as_string += " " + str(time.strftime('%Y-%m-%d', time.localtime(int((rows[0] / 1000000000) + 978307200))))
        counter = Counter(all_dates_as_string.split())
        print(counter)

    def insert_most_frequently_spoken_to(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_most_messages_from(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 0 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        print(self.cur.fetchone())

    def insert_most_messages_to(self):
        command_string = "select PHONE_NUMBER from HANDLE where HANDLE_ID = (select HANDLE_ID from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc) where occurance = (select max(occurance) as most_messages from (select HANDLE_ID, count(HANDLE_ID) as occurance from message where IS_FROM_ME = 1 group by HANDLE_ID order by count(HANDLE_ID) desc)))"
        self.cur.execute(command_string)
        print(self.cur.fetchone())













