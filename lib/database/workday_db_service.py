from lib.database.mysql import MySqlConnection
from uuid import uuid4

class WorkdayDbService:

    def __init__(self):

        self.__conn = MySqlConnection()
        self.workdays_ids = {}

    def get_id_by_datestring(self, date_str: str, day: int, week: int, year: int) -> str:

        id = self.__get_id_dict(day, week, year)
        if id: return id

        date = self.__format_datestr(date_str)

        id = self.__query_workday(date)
        if not id: id = self.__insert_workday(date, day, week, year)

        self.__set_id_dict(id, day, week, year)
        return id


    def __get_id_dict(self, day: int, week: int, year: int) -> str:

        year_keys = self.workdays_ids.keys()
        if not year in year_keys: return None

        week_keys = self.workdays_ids[year].keys()
        if not week in week_keys: return None

        day_keys = self.workdays_ids[year][week].keys()
        if day not in day_keys: return None

        return self.workdays_ids[year][week][day]
    
    def __set_id_dict(self, id: str, day: int, week: int, year: int):
        year_keys = self.workdays_ids.keys()
        if not year in year_keys: self.workdays_ids[year] = {}

        week_keys = self.workdays_ids[year].keys()
        if not week in week_keys: self.workdays_ids[year][week] = {}
        
        self.workdays_ids[year][week][day] = id
    
    def __query_workday(self, date: str):

        query = "SELECT * FROM workday WHERE date = %s"
        values = (date,)

        result = self.__conn.query_one(query, values)
        if result: return result[0]
    
    def __insert_workday(self, date: str, day: int, week: int , year: int):

        command = command = "INSERT INTO workday (id, year, weeknumber, weekday, date) VALUES (%s,%s,%s,%s,%s)"
        values = (str(uuid4()), year, week, day, date)

        self.__conn.command(command, values)
        return values[0]

    def __format_datestr(self, date_str: str):
        date_str = date_str.split(".")  
        date_str.reverse()
        return "-".join(date_str)
