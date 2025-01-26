import os
import mysql.connector
from uuid import uuid4

class MySqlConnection:

    def __init__(self):

        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DATABASE")

        self.connection = mysql.connector.connect(host=host,user=user,password=password,database=database)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def query_one(self, query: str, values: tuple = ()):
        self.cursor.execute(query, values)
        result = self.cursor.fetchone()
        return result

    def query_all(self, query: str, values: tuple = ()):
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result
    
    def command(self, command: str, values: tuple = ()):
        self.cursor.execute(command, values)
        self.connection.commit()

    def command_many(self, command: str, values: list[tuple]):
        self.cursor.executemany(command, values)
        self.connection.commit()




def check_workday(employee_id: str, workday_id: str, shiftcode_id: str):

    db = MySqlConnection()

    query = "SELECT shiftcode_id FROM Shift WHERE employee_id = %s and workday_id = %s order by timestamp desc limit 1"
    values = (employee_id, workday_id,)

    result = db.query_one(query, values)

    if not result:
        return 1, (str(uuid4()), employee_id, workday_id, shiftcode_id,)

    if result[0] == shiftcode_id:
        return 0, None
    
    return 2, (str(uuid4()), employee_id, workday_id, shiftcode_id, )

def insert_workdays(values: list[tuple]):

    db = MySqlConnection()

    command = "INSERT INTO Shift (id, employee_id, workday_id, shiftcode_id, timestamp) values (%s,%s,%s,%s,NOW())"
    db.command_many(command, values)
