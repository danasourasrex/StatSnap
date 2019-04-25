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

    def add_messages_to_db(self, username):
        self.cur.execute("select text, handle_id, is_from_me, date from message")
        acceptable_messages = []
        for rows in self.cur.fetchall():
            acceptable_messages.append([str(rows[0]), str(rows[1]), str(rows[2]), str(rows[3])])
        messageDAO = MessageDAO()
        count = 0
        for rows in acceptable_messages:
            message = Message()
            message.set_values_from_row([str(username), rows[1], self.deEmojify(rows[0]), rows[2], rows[3]])
            messageDAO.batch_insert(message)
            count += 1
            if count % 100 == 0:
                print(count)
            if count > 5000:
                break
        messageDAO.batch_commit()

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
            handle_dao.batch_insert(handle)
        handle_dao.batch_commit()
        print("HANDLES DONE")
        for rows in handle_columns:
            service_look_up = ServiceLookUp()
            service_look_up.set_values_from_row([str(username),str(rows[1]), str(rows[2])])
            service_look_up_dao.batch_insert(service_look_up)
        service_look_up_dao.batch_commit()
        print("ALL DONE")