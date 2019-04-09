import cx_Oracle
from database.DAO import DAO
from database.User import User


class UserDAO(DAO):

    def __init__(self):
        DAO.__init__(self)

    def insert(self, data):
        User.user_instance_checker(data)
        command_string = "insert into STAT_SNAP_USER(USER_ID, PASSWORD) values (" \
                         ":1,:2)"
        self.cur.execute(command_string, (str(data.get_user_id()),
                                          str(data.get_password())))
        self.con.commit()

    def select(self, data):
        command_string = "select USER_ID, PASSWORD from STAT_SNAP_USER where USER_ID = " + str(data)
        self.cur.execute(command_string)
        row = self.cur.fetchone()
        user = User()
        user.set_values_from_row([row[0], row[1]])
        return user


    def delete(self, data):
        command_string = "delete from STAT_SNAP_USER where USER_ID = :1;"
        self.cur.execute(command_string, (str(data)))
        self.con.commit()