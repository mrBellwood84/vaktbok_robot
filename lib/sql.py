import mysql.connector
from uuid import uuid4

from app_config.secret import *

class MySqlConnection:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
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


def get_workday_id(date: str, weekday: int, week_number: int, year: int):
    
    db = MySqlConnection()

    date = __format_date_str(date)

    query = "SELECT * FROM Workday WHERE date = %s"
    values = (date,)
    
    result = db.query_one(query, values)
    if result: return result[0]

    command = "INSERT INTO Workday (id, year, weeknumber, weekday, date) VALUES (%s,%s,%s,%s,%s)"
    values = (str(uuid4()), year, week_number, weekday, date)

    db.command(command, values)
    return values[0]

def get_employee_id(name: str):
    
    db = MySqlConnection()

    query = "SELECT * FROM Employee WHERE name = %s"
    values = (name,)

    result = db.query_one(query, values)
    if result: return result[0]
    
    command = "INSERT INTO Employee (id, name) VALUES (%s, %s)"
    values = (str(uuid4()), name)

    db.command(command, values)
    return values[0]

def get_shiftcode_id(code: str, start: str, end: str):

    db = MySqlConnection()

    query = "SELECT * FROM ShiftCode WHERE code = %s"
    values = (code,)

    result = db.query_one(query, values)
    if result: return result[0]

    command = "INSERT INTO ShiftCode (id, code, start, end) VALUES (%s,%s,%s,%s)"
    values = (str(uuid4()), code, start, end)

    db.command(command, values)

    return values[0]

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


def __format_date_str(date: str):
    date_str = date.split(".")
    date_str.reverse()
    return "-".join(date_str)
