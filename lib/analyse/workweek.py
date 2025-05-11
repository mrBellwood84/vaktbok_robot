from lib.analyse.workday import Workday

class WorkWeek:
    def __init__(self, year, week):
        self.year = year
        self.week = week

        self.workhour_count = 0
        self.workday_count = 0

        self.workday_dict = {}

    
    def add_workday(self, wd:Workday, day:int):
        if wd.worktime == 0: return
        self.workhour_count += wd.worktime
        self.workday_count += 1
        self.workday_dict[day] = wd