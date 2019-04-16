import cx_Oracle


class DAO:

    def __init__(self):
        ip = 'stonehillcsc325.cjjvanphib99.us-west-2.rds.amazonaws.com'
        port = 1521
        SID = 'ORCL'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        self.con = cx_Oracle.connect('mwojtyna', 'csrocks55', dsn_tns)
        self.cur = self.con.cursor()

    def __del__(self):
        self.con.close()

    def select(self, data):
        pass

    def insert(self, data):
        pass

    def update(self, data):
        pass

    def delete(self, data):
        pass
