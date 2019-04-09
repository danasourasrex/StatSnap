from database.DAO import DAO
from database.StatLookup import StatLookup


class StatLookUpDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, data):
        command_string = 'INSERT INTO STAT_LOOKUP (ID, DATA) VALUES  (:1,:2)'
        self.cur.execute(command_string, (str(data.get_ID), str(data.get_DATA)))

    def delete(self, data):
        command_string = 'DELETE FROM STAT_LOOKUP WHERE ID = (:1)'
        self.cur.execute(command_string, (str(data.get_ID)))

    def select(self, data):
        command_string = "SELECT * FROM STAT_LOOKUP WHERE ID = '" + str(data) + "\'"
        self.cur.execute(command_string)
        rows = self.cur.fetchall()
        statLookup = StatLookup()
        statLookup.set_values_from_row(rows)
