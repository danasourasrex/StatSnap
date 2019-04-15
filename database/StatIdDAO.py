from database.DAO import DAO
from database.StatId import StatId


class StatIdDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, data):
        command_string = "INSERT INTO STAT_ID (ID, STAT_ID, HANDLE_ID) VALUES  (:1,:2,:3)"
        self.cur.execute(command_string, (str(data.get_id()),str(data.get_stat_id()), str(data.get_handle_id())))
        self.con.commit()

    def delete(self, data):
        command_string = "DELETE FROM STAT_ID WHERE ID = '" + data + "'"
        self.cur.execute(command_string)
        self.con.commit()

    def select(self, data):
        command_string = "SELECT * FROM STAT_ID WHERE ID = '" + str(data) + "\'"
        self.cur.execute(command_string)
        row = self.cur.fetchall()
        stat_id = StatId()
        stat_id.set_values_from_row(row)
        return stat_id

    def select_all(self):
        command_string = "SELECT * FROM STAT_ID"
        self.cur.execute(command_string)
        list_of_stat_id = []
        for rows in self.cur.fetchall():
            stat_id = StatId()
            stat_id.set_values_from_row(rows)
            list_of_stat_id.append(stat_id)
        return list_of_stat_id



