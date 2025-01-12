from alive_progress import alive_bar
from bs4 import BeautifulSoup
from datetime import datetime
import pyperclip

from lib.driver import WebDriver, WebDriverWait, find_and_click, find_and_input, find_and_element
from lib.sql import get_employee_id, get_workday_id, get_shiftcode_id, check_workday, insert_workdays

from app_config.config import *
from app_config.secret import *

# Itterate workweek and extract 
def itterate_workweek(driver: WebDriver, waiter: WebDriverWait):

    loopguard = 100

    while True:

        loopguard -= 1
        if loopguard <= 0: break

        week_str = find_and_element("week_info_container", waiter, dev_mode=DEV_MODE, explain="Get week info container").text
        curr_week = int(week_str.split(",")[0].split(" ")[1])
        curr_year = int(week_str[-4:])

        if curr_year < START_YEAR: 
            find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")
            print(" >> WARNING :: Current year is lower than start year!")
            continue
        if curr_year == START_YEAR and curr_week < START_WEEK: 
            find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")
            print(" WARNING :: Current week is lower than start week!")
            continue
        if curr_year >= END_YEAR and curr_week > END_WEEK: break

        print(f"\n >> RESOVLING WEEK  {curr_week} | YEAR {curr_year} <<")

        date, work = _extract_week_table(driver, waiter, DEV_MODE)

        result = _harvest_workweek_data(date, work, curr_year, curr_week)

        print(f" - NoChange : {result[0]} | Changed {result[1]} | New {result[2]} - ")

        find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")

def print_workbook_weekly(driver: WebDriver, waiter: WebDriverWait):
    
    loopguard = 100

    while True:
        
        loopguard -= 1
        if loopguard <= 0: break

        week_str = find_and_element("week_info_container", waiter, dev_mode=DEV_MODE, explain="Get week info container").text
        curr_week = int(week_str.split(",")[0].split(" ")[1])
        curr_year = int(week_str[-4:])

        if curr_year < START_YEAR: 
            find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")
            print(" >> WARNING :: Current year is lower than start year!")
            continue
        if curr_year == START_YEAR and curr_week < START_WEEK: 
            find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")
            print(" WARNING :: Current week is lower than start week!")
            continue
        if curr_year >= END_YEAR and curr_week > END_WEEK: break

        filename = "vaktbok_{}_{:02}".format(curr_year, curr_week)
        pyperclip.copy(filename)

        find_and_click("print_week_btn", waiter, dev_mode=DEV_MODE, explain="Click print")

        input("\n ENTER TO CONTINUE! \n")

        find_and_click("next_week_btn", waiter, dev_mode=DEV_MODE, explain="Clicking next week")

def _extract_week_table(driver: WebDriver, waiter: WebDriverWait, dev_mode: bool = False):

    find_and_element("week_table", waiter, dev_mode, explain="Finding week table")

    page = driver.page_source
    soup = BeautifulSoup(page, "lxml")
    date_data = soup.find_all("table")[6]
    work_data = soup.find_all("table")[7]

    return str(date_data), str(work_data)

def _harvest_workweek_data(date_data, work_data, year, week_number):

    new_item = 0
    changed = 0
    no_change = 0

    bulk = []

    date_ids = __parse_dates(date_data, year, week_number)

    workday_soup = BeautifulSoup(work_data, "lxml")
    rows = workday_soup.find_all("tr")

    with alive_bar(len(rows) - 2) as bar:
    
        for row in rows:
            
            content = row.find_all("td")
            content = [t.text for t in content]
            
            name = content[0]
            if not name: continue
            if name == "LEDIG": continue
            employee_id = get_employee_id(name)

            shifts = content[1:]

            for i,v in enumerate(shifts):
                
                code, start, end = __format_shiftcode(v)
                
                workday_id = date_ids[i]
                shiftcode_id = get_shiftcode_id(code, start, end)

                result = check_workday(employee_id, workday_id, shiftcode_id)
            
                if result[0] == 0: no_change += 1
                if result[0] == 1:
                    new_item += 1
                    bulk.append(result[1])
                if result[0] == 2: 
                    changed += 1
                    bulk.append(result[1])

            bar()

    insert_workdays(bulk)
    return no_change, changed, new_item

def __parse_dates(datedata_raw, year, week_number):

    soup = BeautifulSoup(datedata_raw, "lxml")
    rows = soup.find_all("td")

    date_ids = []
    
    for i,v in enumerate(rows[1:]):
        date_str = v.text[-10:]
        workday_id = get_workday_id(date_str, i, week_number, year)
        date_ids.append(workday_id)
    
    return tuple(date_ids)

def __format_shiftcode(code_str: str):

    code_str = code_str.strip()

    if code_str == "": return "","",""
    
    if len(code_str.split("(")) == 1:
        code_str = [str(x).strip() for x in code_str.split("-")]
        return "-".join(code_str), code_str[0], code_str[1]
    
    try:
        int(code_str[0])
        code_str = code_str[13:]
    except ValueError: 
        pass

    try:
        int(code_str[-1])
        code_str = code_str[:-13]
    except ValueError: 
        pass

    code_str = code_str.split("(")
    code = code_str[0].strip()
    
    time = [str(x).strip() for x in code_str[1].split("-")]
    time[1] = time[1][:-1]

    return code, time[0], time[1]
