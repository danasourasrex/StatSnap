import cx_Oracle
from database.DAO import DAO
from database.Handle import Handle


class HandleDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def batch_insert(self, data):
        Handle.handle_instance_checker(data)

        command_string = "insert into HANDLE(HANDLE_ID, PHONE_NUMBER, USER_ID) values (" \
                         ":1,:2,:3)"
        self.cur.execute(command_string, (str(data.get_handle_id()),
                                          str(data.get_phone_number()),
                                          str(data.get_user_id())))

    def batch_commit(self):
        self.con.commit()

    def insert(self, data):
        Handle.handle_instance_checker(data)

        command_string = "insert into HANDLE(HANDLE_ID, PHONE_NUMBER, USER_ID) values (" \
                         ":1,:2,:3)"
        self.cur.execute(command_string, (str(data.get_handle_id()),
                                          str(data.get_phone_number()),
                                          str(data.get_user_id())))
        self.con.commit()

    def select(self, data):
        command_string = "select HANDLE_ID, PHONE_NUMBER, USER_ID from HANDLE where USER_ID = " + str(data.get_user_id()) + " and HANDLE_ID = " + str(data.get_handle_id())
        self.cur.execute(command_string)
        row = self.cur.fetchone()
        handle_to_return = Handle()
        handle_to_return.set_values_from_row(row)
        return handle_to_return

    def delete(self, data):
        command_string = "delete from HANDLE where USER_ID = :1 and HANDLE_ID = :2"
        self.cur.execute(command_string, (str(data.get_user_id()), str(data.get_handle_id())))
        self.con.commit()

    def select_distinct_handle_ids(self, key):
        command_string = "SELECT DISTINCT(HANDLE_ID) FROM MESSAGE WHERE USER_ID = '" + str(key) + "'"
        self.cur.execute(command_string)
        distinct_handle_ids = []
        for rows in self.cur.fetchall():
            distinct_handle_ids.append(str(rows[0]))
        return distinct_handle_ids

    def select_all_distinct_handles_for_user(self, key):
        command_string = "SELECT HANDLE_ID, PHONE_NUMBER FROM HANDLE WHERE USER_ID = \'" + str(key) + "\' order by HANDLE_ID"
        print(command_string)
        self.cur.execute(command_string)
        distinct_handle_ids = []
        for rows in self.cur.fetchall():
            distinct_handle_ids.append([str(rows[0]), str(rows[1])])
        return distinct_handle_ids


