class ServiceLookUp:
    def __init__(self):
        self.__PHONE_NUMBER=''
        self.__SERVICE=''
    def get_phone_number(self):
        return self.__PHONE_NUMBER
    def get_service(self):
        return self.__SERVICE
    def get_dictionary(self):
        return {
            "PHONE_NUMBER":self.get_phone_number(),
            "HANDLE_ID":self.get_service()
        }
    def set_service(self,service):
        self.__SERVICE=service
    def set_phone_number(self,phone_number):
        self.__PHONE_NUMBER=phone_number

    def set_values_from_row(self, row):
        if len(row)!=2:
            raise ValueError("ROw not big enough")
        self.__PHONE_NUMBER=str(row[0])
        self.__SERVICE=str(row[1])