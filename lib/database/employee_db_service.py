from lib.database.mysql import MySqlConnection
from uuid import uuid4

class EmployeeDbService:

    def __init__(self):
        self.__conn = MySqlConnection()
        self.ids_by_name = {}

    def get_id_by_name(self, name: str):

        keys = self.ids_by_name.keys()
        if name in keys: return self.ids_by_name[name]
        
        id = self.__query_id_by_name(name)
        if not id: id = self.__insert(name)

        return id
    
    def __query_id_by_name(self, name: str):

        query = "SELECT * FROM employee WHERE name = %s"
        values = (name,)

        result = self.__conn.query_one(query, values)
        if result: return result[0]

    def __insert(self, name: str):
        command = "INSERT INTO employee (id, name) VALUES (%s, %s)"
        values = (str(uuid4()), name)

        self.__conn.command(command, values)
        return values[0]

    