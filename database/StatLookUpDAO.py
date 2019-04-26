from database.DAO import DAO
from database.StatLookup import StatLookup


class StatLookUpDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def batch_insert(self, data):
        command_string = 'INSERT INTO STAT_LOOKUP (STAT_ID,STAT_NAME , DATA) VALUES  (:1,:2,:3)'
        self.cur.execute(command_string, (str(data.get_stat_id()),  str(data.get_stat_name()), str(data.get_data())))

    def batch_commit(self):
        self.con.commit()

    def delete(self, data):
        command_string = 'DELETE FROM STAT_LOOKUP WHERE STAT_ID = (:1)'
        self.cur.execute(command_string, (str(data.get_stat_id())))
        self.con.commit()

    def select(self, stat_id):
        command_string = "SELECT * FROM STAT_LOOKUP WHERE STAT_ID = " + str(stat_id)
        self.cur.execute(command_string)
        rows = self.cur.fetchone()
        statLookup = StatLookup()
        statLookup.set_values_from_row(rows)
        return statLookup

    def select_general_stats(self):
        command_string = "SELECT * FROM STAT_LOOKUP WHERE STAT_ID = " + str(stat_id)