from lib.database.mysql import MySqlConnection
from uuid import uuid4

class ShiftcodeDbService:

    def __init__(self):
        self.__conn = MySqlConnection()
        self.ids_by_code = {}

    def get_id_by_code(self, code: str, start:str, end: str):

        keys = self.ids_by_code.keys()
        if code in keys: return self.ids_by_code[code]

        id = self.__query_id_by_code(code)
        if not id: return self.__insert(code, start, end)

        return id

    
    def __query_id_by_code(self, code: str):
        
        query = "SELECT * FROM shiftcode WHERE code = %s"
        values = (code,)

        result = self.__conn.query_one(query, values)
        if result: return result[0]

    def __insert(self, code: str, start: str, end: str):
        
        command = "INSERT INTO shiftcode (id, code, start, end) VALUES (%s, %s, %s, %s)"
        values = (str(uuid4()), code, start, end)

        self.__conn.command(command, values)
        return values[0]

