def print_help():

    text = """
    Running application with no arguments will run program with "harvest" option. 

    Arguments:
    - help : Print this...
    - backup : Store data tables from database to CVS files in backup folder.
    - login : Login only, keeps browser window open untill user promt close in command line.
    - harvest : Login and start harvest from current week.
    - wait_harvest : Login and wait harvest until user promt start in command line. Use for setting start week.
    - workbook : Store workbook 
"""

    print(text)
