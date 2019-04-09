from typing import Any


class Message:
    def __init__(self):
        self.__MESSAGE_ID=0
        self.__HANDLE_ID=0
        self.__TEXT_MESSAGE=""
        self.__IS_FROM_ME=0
        self.__DATE_OF_TEXT=""
    def get_message_id(self):
        return self.__MESSAGE_ID
    def get_handle_id(self):
        return self.__HANDLE_ID
    def get_text_message(self):
        return self.__TEXT_MESSAGE
    def get_is_from_me(self):
        return self.__IS_FROM_ME
    def get_date_of_text(self):
        return self.__DATE_OF_TEXT
    def get_dictionary(self):
        return {
            "MESSAGE_ID":self.get_message_id(),
            "HANDLE_ID":self.get_handle_id(),
            "TEXT_MESSAGE":self.get_text_message(),
            "IS_FROM_ME":self.get_is_from_me(),
            "DATE_OF_TEXT":self.get_date_of_text()
        }
    def set_message_id(self,value):
        self.__MESSAGE_ID=value
    def set_handle_id(self,value):
        self.__HANDLE_ID=value
    def set_text_message(self,value):
        self.__TEXT_MESSAGE=value
    def set_is_from_me(self,value):
        self.__IS_FROM_ME=value
    def set_date_of_text(self,value):
        self.__DATE_OF_TEXT=value

    def set_values_from_row(self, row):
        if len(row)!=5:
            raise ValueError("ROw not big enough")
        self.__MESSAGE_ID=str(row[0])
        self.__HANDLE_ID=str(row[1])
        self.__TEXT_MESSAGE=str(row[2])
        self.__IS_FROM_ME=str(row[3])
        self.__DATE_OF_TEXT=str(row[4])

