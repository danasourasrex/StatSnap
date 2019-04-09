class User:

    def __init__(self):
        self.__user_id = ""
        self.__password = ""

    def get_dictionary(self):
        return {"USER_ID": self.get_user_id(),
                "PASSWORD": self.get_password()}

    def set_values_from_row(self, row):
        if len(row) != 2:
            raise ValueError("Row not big enough")
        self.set_user_id(row[0])
        self.set_password(row[1])

    def get_user_id(self):
        return self.__user_id

    def get_password(self):
        return self.__password

    def set_user_id(self, data):
        self.__user_id = data

    def set_password(self, data):
        self.__password = data

    @staticmethod
    def user_instance_checker(item):
        if not isinstance(item, User):
            raise ValueError('Item is not a User')
