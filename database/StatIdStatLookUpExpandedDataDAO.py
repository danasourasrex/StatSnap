from database.DAO import DAO


class StatIdStatLookUpExpandedDataDAO(DAO):

    def return_all_none_stats(self, username):
        command_string = "SELECT * FROM STAT_ID, STAT_LOOKUP WHERE STAT_ID.STAT_ID = STAT_LOOKUP.STAT_ID AND \
        DATA NOT IN 'None' AND STAT_ID.ID = '" + str(username) + "'"
        self.cur.execute(command_string)
        list_of_none_stats = []
        for rows in self.cur.fetchall():
            list_of_none_stats.append([str(rows[0]), str(rows[1]), str(rows[2]), str(rows[3]), str(rows[4]), str(rows[5])])
        return list_of_none_stats

    def return_expanded_data_stats(self, username):
        command_string = "SELECT * FROM STAT_ID, STAT_LOOKUP, EXPANDED_DATA WHERE STAT_ID.STAT_ID = STAT_LOOKUP.STAT_ID AND\
        EXPANDED_DATA.STAT_ID = STAT_LOOKUP.STAT_ID AND\
        STAT_ID.STAT_ID = EXPANDED_DATA.STAT_ID AND\
        STAT_LOOKUP.DATA = 'None' AND\
        STAT_ID.ID = '" + str(username) + "'"
        self.cur.execute(command_string)
        list_of_expanded_data_stats = []
        for rows in self.cur.fetchall():
            list_of_expanded_data_stats.append([str(rows[0]), str(rows[1]), str(rows[2]), str(rows[4]), str(rows[7]), str(rows[8])])
        return list_of_expanded_data_stats


