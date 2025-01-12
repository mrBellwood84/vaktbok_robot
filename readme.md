# Vaktbok Data Collector

Robot for scraping and comparing shifts in in the work schedule **MinGat** for Helse Bergen. 
Robot will use a regular employee account to access the schedule and will only harvest data as showed to the human user. 
Any new or changed shifts are stored to an sql database with a timestamp for extraction of data.

Note this robot is using the Edge web browser. Certain files are excluded for security reasons.

**store_workbook_weekly.py** is an aditional script created for priting out the workbook as a pdf file through the pages own print functionality.
Will open the **_print to file_** dialog in the browers and also add the suggested file name to the system clipboard.
User can use the **[CTRL + V]** function directly in the dialog to set file name :)


## Files exluded

**Files exluded**
- *./lib/login_procedure.py*
- *./app_config/config.py*
- *./app_config/secret.py*

### ./lib/login_procedure.py

```Python
def login_procedure(driver: WebDriver, waiter: WebDriverWaiter):
    # this function must navigate login procedure.
    # used by main script to login
    # must navigate to "vaktbok" then select week view.
    pass
```

### ./app_config/config.py

Configurations for Selenium WebDriver and date span for data harvest.

- ENTRY_URL: string - Start url for script, login page
- WEBDRIVER_OPTIONS: list[string - Arguments for selenuium webdriver.
- DRIVER_TIMEOUT: integer - Seconds for Webdriver timeout
- DEV_MODE: boolean - Development mode active, will promt a "yes | no" in terminal
- START_YEAR: integer - Start year for work schedule
- START_WEEK: integer - Start week number for work schedule
- END_YEAR: integer - End year for work schedule
- END_WEEK: integer - End week number for work schedule


### ./app_config/secret.py

Secret values for login and sql server

_login for internal pages_
- IHELSE_USER : email for ihelse account
- IHELSE_PWD : password for ihelse account


_login for mingat_
- GAT_USER : user anme for gat user
- GAT_PASSWORD : password for gat user


_login for mysql server_
- MYSQL_HOST = db url: str
- MYSQL_USER = db username: str
- MYSQL_PASSWORD = db password: str