class StatLookup:
    def __init__(self):
        self.__ID = 0
        self.__DATA = 0

    def get_ID(self):
        return self.__ID

    def get_DATA(self):
        return self.__DATA

    def get_dict(self):
        return {
            "ID": self.get_ID(),
            "DATA": self.get_DATA()
        }

    def set_ID(self, id):
        self.__ID = id

    def set_DATA(self, data):
        self.__DATA = data

    def set_values_from_row(self, row):
        if len(row) != 2:
            raise ValueError("Row not big enough")
        self.__ID = str(row[0])
        self.__DATA = str(row[1])
