from database.Message import Message
from database.DAO import DAO


class MessageDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, item):
        command_string = "INSERT INTO MESSAGE (USER_ID, HANDLE_ID,TEXT_MESSAGE,IS_FROM_ME,DATE_OF_TEXT)\
         VALUES  (:1,:2,:3,:4,:5)"
        self.cur.execute(command_string, (str(item.get_user_id()), str(item.get_handle_id()), str(item.get_text_message()), \
                                          str(item.get_is_from_me()), str(item.get_date_of_text())))
        self.con.commit()

    def select_by_user_id_and_handle_id(self, user_id, handle_id):
        command_string = "SELECT * FROM MESSAGE where USER_ID = '" + str(user_id) + "' AND HANDLE_ID = " + str(handle_id)
        self.cur.execute(command_string)
        rows = self.cur.fetchall()
        message = Message()
        message.set_values_from_row(rows)
        return message

    def delete(self, user_id):
        command_string = "DELETE FROM MESSAGE WHERE USER_ID= :1"
        self.cur.execute(command_string, (str(user_id)))
        self.con.commit()
