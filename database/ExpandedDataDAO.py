from database.ExpandedData import ExpandedData
from database.DAO import DAO


class ExpandedDataDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def batch_insert(self, item):
        command_string = "INSERT INTO EXPANDED_DATA (STAT_ID, DATA, OCCURRENCES) VALUES  (:1,:2,:3)"
        self.cur.execute(command_string, (item.get_stat_id(), str(item.get_data()), item.get_occurrences()))

    def batch_commit(self):
        self.con.commit()


    def select(self, key):
        command_string = "SELECT * FROM EXPANDED_DATA WHERE STAT_ID = " + str(key)
        self.cur.execute(command_string)
        expanded_data_list = []
        for rows in self.cur.fetchall():
            expanded_data = ExpandedData()
            expanded_data.set_values_from_row(rows)
            expanded_data_list.append(expanded_data)

        return expanded_data_list

    def delete(self, key):
        command_string = "DELETE FROM EXPANDED_DATA WHERE STAT_ID = " + str(key)
        self.cur.execute(command_string)
        self.con.commit()
