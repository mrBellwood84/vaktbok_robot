from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.edge.webdriver import WebDriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import json
from time import sleep
from random import randint

from app_config.config import *

# create webdriver,  configured to look less like a robot...
def create_driver():

    options = Options()
    
    for opt in WEBDRIVER_OPTIONS:
        options.add_argument(opt)
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Edge(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    waiter = WebDriverWait(driver, DRIVER_TIMEOUT)

    return driver, waiter

# search for button and click
def find_and_click(xpath_key: str, driver: WebDriverWait, dev_mode: bool = False, explain: str | None = None):
    
    if dev_mode and explain: print(explain)

    while True:

        xpath = __extract_xpath(xpath_key)
        sleep(__rand_sec())

        try:
            driver.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            if not dev_mode: break

        except KeyboardInterrupt: 
            raise KeyboardInterrupt
        
        except InvalidArgumentException:
            print(f" - Invalid Argument occured | Element for \"{xpath_key}\" not found")
        except TimeoutException:
            print(f" - Timeout occured | Element for \"{xpath_key}\" not found")
        except ElementClickInterceptedException:
            print(f" - Click intercept occured | Something blocked the click for {xpath_key}")
        except ElementNotInteractableException:
            print(f" - Element not interactabal | Could not interact with {xpath_key}")

        if dev_mode:
            correct = __promt_dev_yes_no()
            if correct: break

# search input field and enter text input
def find_and_input(input_text: str, xpath_key: str, driver: WebDriverWait, dev_mode: bool = False, explain: str | None = None):

    if dev_mode and explain: print(explain)

    while True:

        xpath = __extract_xpath(xpath_key)
        sleep(__rand_sec())

        try:
            elem = driver.until(EC.presence_of_element_located((By.XPATH, xpath)))
            elem.clear()
            elem.send_keys(input_text)
            if not dev_mode: break

        except KeyboardInterrupt: 
            raise KeyboardInterrupt
        
        except InvalidArgumentException:
            print(f" - Invalid Argument occured | Element for \"{xpath_key}\" not found")
        except TimeoutException:
            print(f" - Timeout occured | Element for \"{xpath_key}\" not found")
        except ElementClickInterceptedException:
            print(f" - Click intercept occured | Something blocked the click for {xpath_key}")
        except ElementNotInteractableException:
            print(f" - Element not interactabal | Could not interact with {xpath_key}")
    
        if dev_mode:
            correct = __promt_dev_yes_no()
            if correct: break

# search for element and return that element
def find_and_element(xpath_key: str, driver: WebDriverWait, dev_mode: bool = False, explain: str |  None = None):

    if dev_mode and explain: print(explain)

    while True:

        xpath = __extract_xpath(xpath_key)
        sleep(__rand_sec())

        try:
            elem = driver.until(EC.presence_of_element_located((By.XPATH, xpath)))
            if not dev_mode: return elem
    
        except KeyboardInterrupt: 
            raise KeyboardInterrupt
        
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
            correct = __promt_dev_yes_no()
            if correct: return elem


# promt a yes / no answer from user, will not continue before valid answer
def __promt_dev_yes_no():
    while True:
        print("DEV :: Did the right thing happen?")
        answer = input(" yes | no >> ").lower()
        if answer == "yes": return True
        if answer == "no": return False
    
# extract xpath string from elements.json file
def __extract_xpath(keyword: str):
    with open("app_config/elements.json") as file:
        data = json.loads(file.read())

        try: return data[keyword]
        except KeyError: print(f"Keyword {keyword} for element does not exists in \"app_config/elements.json\"")

# return seconds for retry sleep. Set to be between 0.5 and 2 seconds
def __rand_sec(): return randint(7, 25) / 10