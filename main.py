from lib.driver import create_driver
from lib.login_procedure import login_procedure
from lib.spider import itterate_workweek

from app_config.config import *


if __name__ == "__main__":

    driver, waiter = create_driver()
    driver.get(ENTRY_URL)

    login_procedure(driver, waiter)
    itterate_workweek(driver, waiter)

    input(" => LolCat says enter to exit...")