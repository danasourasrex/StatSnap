class Handle:

    def __init__(self):
        self.__handle_id = -1
        self.__phone_number = ""
        self.__user_id = -1

    def get_dictionary(self):
        return {"HANDLE_ID": self.get_handle_id(),
                "PHONE_NUMBER": self.get_phone_number(),
                "USER_ID": self.get_user_id()}

    def set_values_from_row(self, row):
        if len(row) != 3:
            raise ValueError("Row not big enough")
        self.set_handle_id(row[0])
        self.set_phone_number(row[1])
        self.set_user_id(row[2])

    def get_handle_id(self):
        return self.__handle_id

    def get_phone_number(self):
        return self.__phone_number

    def get_user_id(self):
        return self.__user_id

    def set_handle_id(self, data):
        self.__handle_id = data

    def set_phone_number(self, data):
        self.__phone_number = data

    def set_user_id(self, data):
        self.__user_id = data

    @staticmethod
    def handle_instance_checker(item):
        if not isinstance(item, Handle):
            raise ValueError('Item is not a Handle')
