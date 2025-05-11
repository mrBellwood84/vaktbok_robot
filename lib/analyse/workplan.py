from lib.analyse.workday import Workday
from lib.analyse.workweek import WorkWeek

class Workplan:

    def __init__(self, name:str):
        self.name = name

        self.total_workhours = 0

        self.workday_count = 0
        self.workdays_dict = {}

        self.workdays_duplicate_count = 0
        self.workdays_duplicate_dict = {}
        
        self.workdays_below_8_count = 0
        self.workdays_below_8_dict = {}

        self.workdays_above_8_count = 0
        self.workdays_above_8_dict = {}
        
        self.workweek_dict = {}
        

    def add_workday(self, data: tuple):
        date = data[0]
        year = data[1]
        week = data[2]
        day = data[3]
        code = data[4]
        start = data[5]
        end = data[6]
        timestamp = str(data[7])

        workweek_key = f"{year}-{"0" if week < 10 else ""}{week}"

        wd = Workday(date, code, start, end, timestamp)

        if wd.worktime > 0:
            self.workday_count += 1
            self.workdays_dict[date] = wd
            self.total_workhours += wd.worktime
        
        if wd.below_8:
            self.workdays_below_8_count += 1
            self.workdays_below_8_dict[date] = wd
        
        if wd.above_8:
            self.workdays_above_8_count += 1
            self.workdays_above_8_dict[date] = wd

        self.add_to_workweek(wd, workweek_key, year, week, day)

    def add_duplicate(self, data: tuple):
        date = data[0]
        code = data[4]
        start = data[5]
        end = data[6]
        timestamp = str(data[7])

        wd = Workday(date, code, start, end, timestamp)

        self.workdays_duplicate_count += 1
        if date not in self.workdays_duplicate_dict.keys():
            self.workdays_duplicate_dict[date] = []
            self.workdays_duplicate_dict[date].append(wd)

    def add_to_workweek(self, wd: Workday, key: str, year: int, week: int, day: int):

        if key not in self.workweek_dict.keys():
            self.workweek_dict[key] = WorkWeek(year, week)
        
        self.workweek_dict[key].add_workday(wd, day)