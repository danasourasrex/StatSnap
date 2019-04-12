class StatId:

    def __init__(self):
        self.__id = ""
        self.__stat_id = ""
        self.__handle_id = -1

    def get_dictionary(self):
        return {"ID": self.get_id(),
                "STAT_ID": self.get_stat_id(),
                "HANDLE_ID": self.get_handle_id()}

    def set_values_from_row(self, row):
        if len(row) != 3:
            raise ValueError("Row not big enough")
        self.set_id(row[0])
        self.set_stat_id(row[1])
        self.set_handle_id(row[2])

    def get_handle_id(self):
        return self.__handle_id

    def get_stat_id(self):
        return self.__stat_id

    def get_id(self):
        return self.__id

    def set_handle_id(self, data):
        self.__handle_id = data

    def set_stat_id(self, data):
        self.__stat_id = data

    def set_id(self, data):
        self.__id = data

    @staticmethod
    def handle_instance_checker(item):
        if not isinstance(item, StatId):
            raise ValueError('Item is not a StatId')
