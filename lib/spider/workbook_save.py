import os, pyperclip

from app_config.config import *
from lib.spider import Driver


class WorkbookSave:

    def __init__(self, driver: Driver):
        self.__driver = driver
    
    def save(self, dev_mode: bool = False):

        print(" -> Set initial week in browser! ")
        input(" -- Press 'ENTER' to start saving workbooks --")

        while True:

            week, year = self.__parseWeekStr(dev_mode)

            if year >= END_YEAR and week > END_WEEK: break

            filename = "vaktbok_{}_{:02}".format(year, week)
            pyperclip.copy(filename)

            self.__driver.findAndClick("print_week_btn", dev_mode, "Clicking print.")

            os.system("cls")
            print("\n -> saving {}".format(filename))
            input(" -> Press 'ENTER' to continue... ")

            self.__driver.findAndClick("next_week_btn", dev_mode, "Clicking next week.")
    
    def __parseWeekStr(self, dev_mode: bool):
        week_str = self.__driver.findElement("week_info_container", dev_mode, explain="Get week info container").text
        curr_week = int(week_str.split(",")[0].split(" ")[1])
        curr_year = int(week_str[-4:]) 
        return curr_week, curr_year
