
from database.MessageDAO import MessageDAO
from database.Message import Message
from database.Handle import Handle
from database.HandleDAO import HandleDAO
from database.ServiceLookUp import ServiceLookUp
from database.ServiceLookUpDAO import ServiceLookUpDAO
import sqlite3

class ChatDBtoOracle():

    def __init__(self):
        self.conn = sqlite3.connect("db_upload/chat.db")
        self.cur = self.conn.cursor()

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

    def add_handles_to_db(self, username):
        self.cur.execute("select ROWID, id, service from handle")
        handle_dao = HandleDAO()
        service_look_up_dao = ServiceLookUpDAO()
        handle_columns = []
        for rows in self.cur.fetchall():
            handle_columns.append([str(rows[0]), str(rows[1]), str(rows[2])])
        for rows in handle_columns:
            handle = Handle()
            handle.set_values_from_row([str(rows[0]), str(rows[1]), str(username)])
            handle_dao.insert(handle)
        for rows in handle_columns:
            service_look_up = ServiceLookUp()
            service_look_up.set_values_from_row([str(rows[1]), str(rows[2])])
            service_look_up_dao.insert(service_look_up)









