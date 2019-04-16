from database.ExpandedData import ExpandedData
from database.DAO import DAO


class ExpandedDataDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, item):
        command_string = "INSERT INTO EXPANDED_DATA (STAT_ID, DATA, OCCURRENCES) VALUES  (:1,:2,:3)"
        self.cur.execute(command_string, (str(item.get_stat_id), str(item.get_data), str(item.get_occurrences())))
        self.con.commit()

    def select(self, key):
        command_string = "SELECT * FROM EXPANDED_DATA WHERE STAT_ID = " + str(key)
        self.cur.execute(command_string)
        row = self.cur.fetchone()
        expanded_data = ExpandedData()
        expanded_data.set_values_from_row(row)
        return expanded_data

    def delete(self, key):
        command_string = "DELETE FROM EXPANDED_DATA WHERE STAT_ID = " + str(key)
        self.cur.execute(command_string)
        self.con.commit()
