def print_help():

    text = """
    Running application with no arguments will run program with "harvest" option. 

    Arguments:
    - backup : Store database to CVS files.
    - login : Run login procedure only
    - harvest : Login and start harvest from current week.
    - wait : Login and await data harvest until user promt
    - workbook : Store workbook 
    """

    print(text)
