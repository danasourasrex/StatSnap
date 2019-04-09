import cx_Oracle
from database.DAO import DAO
from database.Handle import Handle


class HandleDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def insert(self, data):
        Handle.handle_instance_checker(data)

        command_string = "insert into HANDLE(HANDLE_ID, PHONE_NUMBER, USER_ID) values (" \
                         ":1,:2,:3)"
        self.cur.execute(command_string, (str(data.get_handle_id()),
                                          str(data.get_phone_number()),
                                          str(data.get_user_id())))
        self.con.commit()

    def select(self, data):
        command_string = "select HANDLE_ID, PHONE_NUMBER, USER_ID from HANDLE where USER_ID = " + str(data[0]) + " and HANDLE_ID = " + str(data[1])
        self.cur.execute(command_string)
        row = self.cur.fetchone()
        handle_to_return = Handle()
        handle_to_return.set_values_from_row(row)
        return handle_to_return

    def delete(self, data):
        command_string = "delete * from HANDLE where USER_ID = :1 and HANDLE_ID = :2;"
        self.cur.execute(command_string, (str(data[0]), str(data[1])))
        self.con.commit()

