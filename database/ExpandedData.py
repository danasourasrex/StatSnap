
class ExpandedData:
    def __init__(self):
        self.__STAT_ID = 0
        self.__DATA = ""
        self.__OCCURRENCES = 0

    def get_stat_id(self):
        return self.__STAT_ID

    def get_data(self):
        return self.__DATA

    def get_occurrences(self):
        return self.__OCCURRENCES

    def get_dictionary(self):
        return {
            "STAT_ID": self.get_stat_id(),
            "DATA": self.get_data(),
            "OCCURRENCES": self.get_occurrences()
        }

    def set_stat_id(self, value):
        self.__STAT_ID = value

    def set_data(self, value):
        self.__DATA = value

    def set_occurrences(self, value):
        self.__OCCURRENCES = value


    def set_values_from_row(self, row):
        if len(row) != 3:
            raise ValueError("Row not big enough")
        self.__STAT_ID = str(row[0])
        self.__DATA = str(row[1])
        self.__OCCURRENCES = str(row[2])

