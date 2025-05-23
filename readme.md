# Vaktbok Data Collector

Robot for scraping and comparing shifts in in the work schedule **MinGat** for Helse Bergen.
Robot will use a regular employee account to access the schedule and will only harvest data as showed to the human user.
Any new or changed shifts are stored to an sql database with a timestamp for extraction of data.

Note this robot is using the Edge web browser. Certain files are excluded for security reasons.

### Store Workbook

Store workbook option will itterate workweek on schedule.
Will open the **_print to file_** dialog in the browers and also add the suggested file name to the system clipboard.
User can use the **[CTRL + V]** function directly in the dialog to set file name :)

### Options

Adding argued options will decide program behaviour. If no arguments are added, robot will run with **harvest** argument.

- **help** : Print something like this...
- **backup** : Store data tables from database to CVS files in backup folder.
- **login** : Login only, keeps browser window open untill user promt close in command line.
- **harvest** : Login and start harvest from current week.
- **wait** : Login and wait harvest until user promt start in command line. Use for setting start week.
- **workbook** : Store workbook

## Excluded files and Environment variables

_Files exluded_

- _./app_config/config.py_

### ./app_config/config.py

Configurations for Selenium WebDriver and date span for data harvest.

- ENTRY_URL: string - Start url for script, login page
- WEBDRIVER_OPTIONS: list[string - Arguments for selenuium webdriver.
- DRIVER_TIMEOUT: integer - Seconds for Webdriver timeout
- START_YEAR: integer - Start year for work schedule
- START_WEEK: integer - Start week number for work schedule
- END_YEAR: integer - End year for work schedule
- END_WEEK: integer - End week number for work schedule

### Environment variables

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
