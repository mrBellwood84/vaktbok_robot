import csv, datetime, os
from lib.sql import MySqlConnection

class DbBackup:

    _BACKUP_VALUES = [
        {
            "query": "SELECT * FROM employee",
            "columns": ("id", "name"),
            "filename": "backup_employee"
        },    
        {
            "query": "SELECT * FROM workday",
            "columns": ("id", "year", "weeknumber", "weekday", "date"),
            "filename": "backup_workday"
        },    
        {
            "query": "SELECT * FROM shiftcode",
            "columns": ("id", "code", "start", "end"),
            "filename": "backup_shiftcode"
        },    
        {
            "query": "SELECT * FROM shift",
            "columns": ("id","employee_id", ""),
            "filename": "backup_shift"
        },
    ]

    def __init__(self):
        self.__connection = MySqlConnection()
        self.__create_backup_folder()
    
    def execute(self):

        for item in self._BACKUP_VALUES:
            dataset = self.__connection.query_all(item["query"])
            datadict = self.__data_to_dict(dataset, item["columns"])
            filename = self.__complete_file_name(item["filename"])
            self.__write_backup(item["columns"], datadict, filename)
            
    def __write_backup(self, headers, data_dict, file_name):
        with open(file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(data_dict)

    def __create_backup_folder(self):
        now = datetime.datetime.now().date().__str__().replace("-","_")
        path = os.path.join("backup",now)
        if not os.path.exists(path):
            os.makedirs(path)

    def __complete_file_name(self, file_name):
        now = datetime.datetime.now().date().__str__().replace("-","_")
        return f"backup/{now}/{file_name}.csv"

    def __data_to_dict(self, data: set, keys: list):
        result = []
        for item in data:
            item_dict = {}
            for index, key in enumerate(keys):
                item_dict[key] = item[index]
            result.append(item_dict)
        return result
