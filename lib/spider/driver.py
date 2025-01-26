from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import json, random, time

# Configuration import
from app_config.config import *

class Driver:

    def __init__(self):

        self.createDriver()

    def createDriver(self):
         
        options = Options()

        # add options from configuration
        for opt in WEBDRIVER_OPTIONS:
            options.add_argument(opt)

        # options to "hide" robot features
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Edge(options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.waiter = WebDriverWait(self.driver, DRIVER_TIMEOUT)

        self.driver.get(ENTRY_URL)

    def findElement(self, xpath_key: str, dev_mode: bool = False, explain: str | None  = None):

        if dev_mode and explain: print("\n", explain)

        while True:

            xpath = self.__extract_xpath(xpath_key)
            time.sleep(self.__rand_sec())

            try:
                elem = self.waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
                if not dev_mode: return elem

            except KeyboardInterrupt: raise KeyboardInterrupt

            except InvalidArgumentException:
                print(f" - Invalid Argument occured | Element for \"{xpath_key}\" not found")
            except TimeoutException:
                print(f" - Timeout occured | Element for \"{xpath_key}\" not found")
            except ElementClickInterceptedException:
                print(f" - Click intercept occured | Something blocked the click for {xpath_key}")
            except ElementNotInteractableException:
                print(f" - Element not interactabal | Could not interact with {xpath_key}")

            if dev_mode:
                print(elem.get_attribute("innerHTML"), "\n\nIs this what you was looking for?")
                correct = self.__promt_dev_yes_no()
                if correct: return elem
        
    def findAndClick(self, xpath_key: str, dev_mode: bool = False, explain: str | None = None):

        if dev_mode and explain: print("\n", explain)

        while True:
            xpath = self.__extract_xpath(xpath_key)
            time.sleep(self.__rand_sec())

            try:
                self.waiter.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
                if not dev_mode: return
            
            except KeyboardInterrupt: raise KeyboardInterrupt

            except InvalidArgumentException:
                print(f" - Invalid Argument occured | Element for \"{xpath_key}\" not found")
            except TimeoutException:
                print(f" - Timeout occured | Element for \"{xpath_key}\" not found")
            except ElementClickInterceptedException:
                print(f" - Click intercept occured | Something blocked the click for {xpath_key}")
            except ElementNotInteractableException:
                print(f" - Element not interactabal | Could not interact with {xpath_key}")

            if dev_mode:
                correct = self.__promt_dev_yes_no()
                if correct: break

    def findAndInput(self, input_text: str, xpath_key: str, dev_mode: bool = False, explain: str | None = None):

        if dev_mode and explain: print("\n", explain)

        while True:

            xpath = self.__extract_xpath(xpath_key)
            time.sleep(self.__rand_sec())

            try:
                elem = self.waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
                elem.clear()
                elem.send_keys(input_text)
                if not dev_mode: break

            except KeyboardInterrupt: raise KeyboardInterrupt
            
            except InvalidArgumentException:
                print(f" - Invalid Argument occured | Element for \"{xpath_key}\" not found")
            except TimeoutException:
                print(f" - Timeout occured | Element for \"{xpath_key}\" not found")
            except ElementClickInterceptedException:
                print(f" - Click intercept occured | Something blocked the click for {xpath_key}")
            except ElementNotInteractableException:
                print(f" - Element not interactabal | Could not interact with {xpath_key}")
        
            if dev_mode:
                correct = self.__promt_dev_yes_no()
                if correct: break

    def __promt_dev_yes_no(self):
        while True:
            print("DEV :: Did the right thing happen?")
            answer = input(" yes | no >> ").lower()
            if answer == "yes": return True
            if answer == "no": return False
    
    def __extract_xpath(self, keyword: str):
        with open("app_config/elements.json") as file:
            data = json.loads(file.read())

            try: return data[keyword]
            except KeyError: print(f"Keyword {keyword} for element does not exists in \"app_config/elements.json\"")
    
    def __rand_sec(self):
        return random.randint(7, 25) / 10
