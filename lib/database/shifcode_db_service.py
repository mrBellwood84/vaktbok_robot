from lib.database.mysql import MySqlConnection
from uuid import uuid4

class ShiftcodeDbService:

    def __init__(self):
        self.__conn = MySqlConnection()


    def get_id(self, code:str, start:str, end:str):

        query = "SELECT * FROM shiftcode WHERE code = %s AND start = %s AND end = %s"
        values = (code, start, end)

        result = self.__conn.query_one(query, values)

        if result: return result[0]
        return self.__insert(code, start, end)


    def __insert(self, code: str, start: str, end: str):
        
        command = "INSERT INTO shiftcode (id, code, start, end) VALUES (%s, %s, %s, %s)"
        values = (str(uuid4()), code, start, end)

        self.__conn.command(command, values)
        return values[0]

