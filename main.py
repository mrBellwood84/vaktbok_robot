import os, sys
from dotenv import load_dotenv
from lib.database import DbBackup
from lib.spider import Driver, PageProcedures, WorkbookHarvest, WorkbookSave
from lib.help import print_help


FLAGS = ["backup", "login", "harvest", "wait", "workbook"]


def load_arg():
    args = sys.argv[1:]
    if len(args) == 0: return "harvest"
    return args[0].lower()

def run_backup():
    print("\n -- RUNNING BACKUP --")
    dbBackup = DbBackup()
    dbBackup.execute()
    print("-- BACKUP COMPLETE --\n")


def main():
    
    arg = load_arg()
    
    if arg not in FLAGS:
        print_help()
        return

    if arg == "backup":
        run_backup()
        return
    
    driver = Driver()
    pageProc = PageProcedures(driver)
    pageProc.login()

    if arg == "login":
        os.system("cls")
        print("\n -- Login only session started...\n")
        input(" -- Press 'ENTER' to close browser --")
        return
    
    pageProc.gotoVaktbok()
    os.system("cls")

    if arg == "workbook":
        print(" -- Starting workbook save session --\n")
        workbook = WorkbookSave(driver)
        workbook.save()
        return
    
    if arg == "wait":
        input(" -- Press 'ENTER' to start harvest ---")

    if arg == "wait" or "harvest":
        print(" -- Harvesting Vaktbok data --\n")
        harvester = WorkbookHarvest(driver)
        harvester.harvest()
        return


if __name__ == "__main__":

    load_dotenv()
    
    main()