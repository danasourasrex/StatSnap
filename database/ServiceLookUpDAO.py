from database.DAO import DAO
from database.ServiceLookUp import ServiceLookUp


class ServiceLookUpDAO(DAO):
    def __init__(self):
        DAO.__init__(self)

    def insert(self, item):
        command_string = 'INSERT INTO SERVICE_LOOKUP (PHONE_NUMBER, SERVICE) VALUES  (:1,:2)'
        self.cur.execute(command_string, (str(item.get_phone_number()), str(item.get_service())))

    def delete(self, data):
        command_string = 'DELETE FROM SERVICE_LOOKUP WHERE PHONE_NUMBER= (:1)'
        self.cur.execute(command_string, (str(data.get_phone_number())))

    def select(self, data):
        command_string = "SELECT * FROM SERVICE_LOOKUP WHERE PHONE_NUMBER = '" + str(data) + "\'"
        self.cur.execute(command_string)
        rows = self.cur.fetchall()
        service_lookup = ServiceLookUp()
        service_lookup.set_values_from_row(rows)
        return service_lookup
