import sys

from lib.backup import DbBackup
from lib.driver import create_driver
from lib.help import print_help
from lib.login_procedure import login_procedure, goto_vaktbok
from lib.spider import itterate_workweek, print_workbook_weekly

from app_config.config import *

FLAGS = [
    "help",
    "backup",
    "login",
    "harvest",
    "wait_harvest",
    "workbook"
]

def run_main():

    args = sys.argv[1:]

    if len(args) == 0: arg = "harvest"
    else: arg = args[0].lower()

    if arg not in FLAGS or arg == "help":
        print_help()
        return
    
    
    # run db backup
    if arg == "backup":
        run_backup()
        return

    # create session here
    driver, waiter = create_driver()
    driver.get(ENTRY_URL)
    login_procedure(driver, waiter)

    # run login
    if arg == "login":
        input("-- Press enter to close session")
        return

    # run login with harvest from this week
    if arg == "harvest":
        goto_vaktbok(waiter)
        itterate_workweek(driver, waiter)

    # run login with break before harvest
    if arg == "wait_harvest":
        input(" -- Press Enter to start harvest")
        goto_vaktbok(waiter)
        itterate_workweek(driver, waiter)

    if arg == "workbook":
        input(" -- Press enter to start workbook --")
        goto_vaktbok(waiter)
        input(" -- Press Enter to start workbook procedure...")
        print_workbook_weekly(driver, waiter)
        

def run_backup():
    print("\n -- RUNNING BACKUP --")
    dbBackup = DbBackup()
    dbBackup.execute()
    print("-- BACKUP COMPLETE --\n")


if __name__ == "__main__":

    run_main()