from alive_progress import alive_bar
from bs4 import BeautifulSoup

from lib.database import EmployeeDbService, ShiftcodeDbService, ShiftDbService, WorkdayDbService
from lib.spider import Driver

from app_config.config import *


class WorkbookHarvest:

    def __init__(self, driver: Driver):
        
        self.new = 0
        self.changed = 0
        self.unchanged = 0
        
        self.__driver = driver

        self.employeeService = EmployeeDbService()
        self.shiftService = ShiftDbService()
        self.shiftcodeService = ShiftcodeDbService()
        self.workdayService = WorkdayDbService()


    def harvest(self, dev_mode: bool = False):
        
        while True:

            week, year = self.__parse_week_string(dev_mode)
            if year >= END_YEAR and week > END_WEEK: break

            self.__parse_workweek(week, year, dev_mode)

            self.__driver.findAndClick("next_week_btn", dev_mode, "Click next week.")
        
        report = f""" -- VAKTBOK REPORT
    Unchanged : {self.unchanged}
    Changed ..: {self.changed}
    New ......: {self.new}
        """
        
        print(report)


    def __parse_week_string(self, dev_mode: bool):
        week_str = self.__driver.findElement("week_info_container", dev_mode, explain="Get week info container").text
        curr_week = int(week_str.split(",")[0].split(" ")[1])
        curr_year = int(week_str[-4:]) 
        return curr_week, curr_year
    
    def __parse_workweek(self, week, year, dev_mode):

        print(" -- Resolving Week {} | {}".format(week, year))
        
        self.shiftService.init_workweeks(week, year)
        date_data, shift_data = self.__extract_weekly_table(dev_mode)

        all_workday_ids = self.__get_all_workday_ids(date_data, week, year)
        table_rows = BeautifulSoup(shift_data, "lxml").findAll("tr")

        noChange = 0
        change = 0
        new = 0

        shift_bulk = []

        for row in table_rows:
            content = [t.text for t in row.findAll("td")]
            name = content[0]

            if not name: continue
            if name == "LEDIG": continue

            employee_id = self.employeeService.get_id_by_name(name)
            shifts = content[1:]

            for i,v in enumerate(shifts):

                workday_id = all_workday_ids[i]
                shiftcode_id = self.__get_shiftcode_id(v)
                result_code, result_data = self.shiftService.check_shift(workday_id, employee_id, shiftcode_id)

                if result_code == 0: noChange += 1
                if result_code == 1: new += 1; shift_bulk.append(result_data)
                if result_code == 2: change += 1; shift_bulk.append(result_data)
                

        self.shiftService.insert_shift_bulk(shift_bulk)
        self.unchanged += noChange
        self.changed += change
        self.new += new

        result_text = f" -- RESULT -> Unchanged :{noChange} | Changed: {change} | New: {new}\n"
        print(result_text)
            

    def __extract_weekly_table(self, dev_mode: bool = True):
        self.__driver.findElement("week_table", dev_mode, "Finding weekly table")

        page = self.__driver.driver.page_source
        soup = BeautifulSoup(page, "lxml")
        date_data = soup.findAll("table")[6]
        work_data = soup.findAll("table")[7]

        return str(date_data), str(work_data)

    def __get_all_workday_ids(self, data: str, week: int, year: int):

        date_ids = []

        soup = BeautifulSoup(data, "lxml")
        rows = soup.findAll("td")

        for i,v in enumerate(rows[1:]):
            date_str = v.text[-10:]
            workday_id = self.workdayService.get_id_by_datestring(date_str, i, week, year)
            date_ids.append(workday_id)
        
        return tuple(date_ids)
    
    def __parse_shift_code(self, code_str: str):

        code_str = code_str.strip().replace(" ","")

        if code_str == "": return "","",""

        if code_str.find("(") == -1:
            return "no-code", code_str[:5], code_str[-5:]

        while code_str[2] == ":": code_str = code_str[11:]
        while code_str[-3] == ":": code_str = code_str[:-11]

        code = code_str[0:code_str.find("(")]
        start = code_str[-12:-7]
        end = code_str[-6:-1]

        return code, start, end

   
    def __get_shiftcode_id(self, raw_data: str):
        code, start, end = self.__parse_shift_code(raw_data)
        return self.shiftcodeService.get_id(code, start, end)

