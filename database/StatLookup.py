class StatLookup:
    def __init__(self):
        self.__ID = 0
        self.__STAT_ID = 0
        self.__STAT_NAME = 0
        self.__DATA = 0
        self.__HANDLE_ID = 0


    def get_id(self):
        return self.__ID

    def get_stat_id(self):
        return self.__STAT_ID

    def get_stat_name(self):
        return self.__STAT_NAME

    def get_data(self):
        return self.__DATA

    def get_handle_id(self):
        return self.__HANDLE_ID

    def get_dict(self):
        return {
            "ID": self.get_id(),
            "STAT_ID": self.get_stat_id(),
            "STAT_NAME": self.get_stat_name(),
            "DATA": self.get_data(),
            "HANDLE_ID": self.get_handle_id()
        }

    def set_ID(self, id):
        self.__ID = id

    def set_DATA(self, data):
        self.__DATA = data

    def set_stat_id(self, data):
        self.__STAT_ID = data

    def set_stat_name(self, data):
        self.__STAT_NAME = data

    def set_handle_id(self, data):
        self.__HANDLE_ID = data

    def set_values_from_row(self, row):
        if len(row) != 5:
            raise ValueError("Row not big enough")
        self.__ID = str(row[0])
        self.__STAT_ID = str(row[1])
        self.__STAT_NAME = str(row[2])
        self.__DATA = str(row[3])
        self.__HANDLE_ID = str(row[4])
