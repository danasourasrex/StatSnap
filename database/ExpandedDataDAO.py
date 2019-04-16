from database.ExpandedData import ExpandedData
from database.DAO import DAO


class ExpandedDataDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, item):
        command_string = "INSERT INTO EXPANDED_DATA (STAT_ID, DATA, OCCURRENCES) VALUES  (:1,:2,:3)"
        self.cur.execute(command_string, (str(item.get_stat_id), str(item.get_data), str(item.get_occurrences())))
        self.con.commit()
