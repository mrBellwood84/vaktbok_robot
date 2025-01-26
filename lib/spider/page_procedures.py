import os, time
from lib.spider import Driver


class PageProcedures:

    def __init__(self, driver: Driver):
        self.__driver = driver
    

    def login(self, dev_mode: bool = False):

        ihelse_user = os.getenv("IHELSE_USER")
        ihelse_pass = os.getenv("IHELSE_PWD")
        gat_user = os.getenv("GAT_USER")
        gat_pass = os.getenv("GAT_PASSWORD")

        self.__driver.findAndInput(ihelse_user, "ihelse_user_input", dev_mode, "Enter username for ihelse account.")
        self.__driver.findAndClick("ihelse_user_next", dev_mode, "Click next after user input.")
        self.__driver.findAndInput(ihelse_pass, "ihelse_pwd_input", dev_mode, "Enter password for ihelse account.")
        self.__driver.findAndClick("ihelse_pwd_next", dev_mode, "Click next after password input.")

        while True:
            if self.__driver.driver.current_url == "https://login.microsoftonline.com/common/SAS/ProcessAuth": 
                break
            print("Awaiting authentification")
            time.sleep(3)
        self.__driver.findAndClick("ihelse_staylogin_btn", dev_mode, explain="Click away 'stay logged in' box.")

        self.__driver.findAndInput(gat_user, "gat_user_input", dev_mode, "Enter GAT username.")
        self.__driver.findAndInput(gat_pass, "gat_pwd_input", dev_mode, "Enter GAT password.")
        self.__driver.findAndClick("gat_login_btn", dev_mode, explain="Click to login.")

        self.__driver.findAndClick("cookie_close_btn", dev_mode, "Close cookie banner")
        
    
    def gotoVaktbok(self, dev_mode: bool = False):
        self.__driver.findAndClick("vaktbok_btn", dev_mode, "Click 'Vaktbok' menu item.")
        self.__driver.findAndClick("vaktbok_weekview", dev_mode, "Click week view for 'Vaktbok'")
