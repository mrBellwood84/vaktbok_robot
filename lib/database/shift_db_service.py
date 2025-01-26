from lib.database.mysql import MySqlConnection
from uuid import uuid4

class ShiftDbService:

    def __init__(self):
        self.__conn = MySqlConnection()
        self.__shifts = {}

    def init_workweeks(self, week, year):

        self.__shifts = {}

        query = "SELECT s.workday_id, s.employee_id, s.shiftcode_id, s.timestamp FROM shift AS s JOIN workday AS w ON s.workday_id = w.id WHERE w.weeknumber = %s AND year = %s"
        values = (week, year)

        data = self.__conn.query_all(query, values)

        for item in data:

            workday_id = item[0]
            employee_id = item[1] 
            shiftcode_id = item[2]
            timestamp = item[3]

            if workday_id not in self.__shifts.keys(): self.__shifts[workday_id] = {}

            if employee_id not in self.__shifts[workday_id].keys():
                self.__shifts[workday_id][employee_id] = (shiftcode_id, timestamp)
                continue

            if timestamp > self.__shifts[workday_id][employee_id][1]:
                self.__shifts[workday_id][employee_id] = (shiftcode_id, timestamp)
                continue
        
    def check_shift(self, workday_id, employee_id, shiftcode_id):

        last_shiftcode = self.__get_shift_dict(workday_id, employee_id)

        if not last_shiftcode: 
            return 1, (str(uuid4()), employee_id, workday_id, shiftcode_id)
        
        if last_shiftcode != shiftcode_id: 
            return 2, (str(uuid4()), employee_id, workday_id, shiftcode_id)
        
        return 0, None


    def insert_shift_bulk(self, data: list[tuple]):

        command = "INSERT INTO Shift (id, employee_id, workday_id, shiftcode_id, timestamp) values (%s,%s,%s,%s,NOW())"
        self.__conn.command_many(command, data)


    def __get_shift_dict(self, workday_id, employee_id):
        workday_keys = self.__shifts.keys()
        if workday_id not in workday_keys: return None

        employee_keys = self.__shifts[workday_id].keys()
        if employee_id not in employee_keys: return None

        return self.__shifts[workday_id][employee_id][0]
