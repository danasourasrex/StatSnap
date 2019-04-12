class StatLookup:
    def __init__(self):
        self.__STAT_ID = 0
        self.__STAT_NAME = 0
        self.__DATA = 0

    def get_stat_id(self):
        return self.__STAT_ID

    def get_stat_name(self):
        return self.__STAT_NAME

    def get_data(self):
        return self.__DATA

    def get_dict(self):
        return {"STAT_ID": self.get_stat_id(),
                "STAT_NAME": self.get_stat_name(),
                "DATA": self.get_data()
        }

    def set_data(self, data):
        self.__DATA = data

    def set_stat_id(self, data):
        self.__STAT_ID = data

    def set_stat_name(self, data):
        self.__STAT_NAME = data


    def set_values_from_row(self, row):
        if len(row) != 3:
            raise ValueError("Row not big enough")
        self.__STAT_ID = str(row[0])
        self.__STAT_NAME = str(row[1])
        self.__DATA = str(row[2])
