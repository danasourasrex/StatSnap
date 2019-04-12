from database.DAO import DAO
from database.StatLookup import StatLookup


class StatLookUpDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, data):
        command_string = 'INSERT INTO STAT_LOOKUP (ID, STAT_ID, STAT_NAME, DATA, HANDLE_ID) VALUES  (:1,:2,:3,:4,:5)'
        self.cur.execute(command_string, (str(data.get_id()), str(data.get_stat_id()), str(data.get_stat_name()), str(data.get_data()), str(data.get_handle_id())))
        self.con.commit()

    def delete(self, data):
        command_string = 'DELETE FROM STAT_LOOKUP WHERE ID = (:1) and STAT_ID = (:2) and HANDLE_ID = (:3)'
        self.cur.execute(command_string, (str(data.get_id()), str(data.get_stat_id()), str(data.get_handle_id())))
        self.con.commit()

    def select(self, id, stat_id, handle_id):
        command_string = "SELECT * FROM STAT_LOOKUP WHERE ID = " + id + " and STAT_ID = " + stat_id + " and HANDLE_ID = " + handle_id
        self.cur.execute(command_string)
        rows = self.cur.fetchall()
        statLookup = StatLookup()
        statLookup.set_values_from_row(rows)
