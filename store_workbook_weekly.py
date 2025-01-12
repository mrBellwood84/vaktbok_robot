from lib.driver import create_driver
from lib.login_procedure import login_procedure
from lib.spider import print_workbook_weekly

from app_config.config import *


if __name__ == "__main__":
    driver, waiter = create_driver()
    driver.get(ENTRY_URL)

    login_procedure(driver, waiter)

    print("\n >> Filenames stored to clipboard, just press CTRL+V to paste  <<\n")

    print_workbook_weekly(driver, waiter)

    input(" >> Lolcat says enter to exit...")

