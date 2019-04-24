class ServiceLookUp:

    def __init__(self):
        self.__USER_ID = ""
        self.__PHONE_NUMBER = ""
        self.__SERVICE = ""

    def get_user_id(self):
        return self.__USER_ID

    def get_phone_number(self):
        return self.__PHONE_NUMBER

    def get_service(self):
        return self.__SERVICE

    def get_dictionary(self):
        return {"PHONE_NUMBER": self.get_phone_number(),
                "HANDLE_ID": self.get_service()}

    def set_service(self, service):
        self.__SERVICE = service

    def set_user_id(self, username):
        self.__USER_ID = username

    def set_phone_number(self, phone_number):
        self.__PHONE_NUMBER = phone_number

    def set_values_from_row(self, row):
        if len(row) != 3:
            raise ValueError("Row not big enough")
        self.__USER_ID = str(row[0])
        self.__PHONE_NUMBER = str(row[1])
        self.__SERVICE = str(row[2])
