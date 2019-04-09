
from database.MessageDAO import MessageDAO
from database.Message import Message
from database.Handle import Handle
from database.HandleDAO import HandleDAO
import sqlite3

class ChatDBtoOracle():

    def __init__(self):
        connection = sqlite3.connect("db_upload/chat.db")
        self.cur = connection.cursor()

    def deEmojify(self, inputString):
        return inputString.encode('ascii', 'ignore').decode('ascii')

    def add_messages_to_db(self):
        self.cur.execute("select text, handle_id, is_from_me, date from message")
        i = 0
        acceptable_messages = []
        for rows in self.cur.fetchall():
            if i == 120:
                break
            elif str(rows[1]) != "32" and "quiz" not in str(rows[0]) and "algorithms" not in str(rows[0]):
                i += 1
                acceptable_messages.append([str(rows[0]), str(rows[1]), str(rows[2]), str(rows[3])])
        messageDAO = MessageDAO()
        for rows in acceptable_messages:
            message = Message()
            message.set_values_from_row([0, rows[1], self.deEmojify(rows[0]), rows[2], rows[3]])
            messageDAO.insert(message)





