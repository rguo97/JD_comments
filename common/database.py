import pymysql
from common.constant import Mysql
import json
class Database:

    def __init__(self,database):
        self.database=database

    def insert_data(self):
        pass

    def update_data(self):
        pass

    def select_data(self):
        pass

    def select_all_date(self):
        pass

    def close_database(self):
        self.database_use.close()

    def get_row_num(self):
        pass

    def get_stats(self):
        tmp_today={}
        line = self.stats.read()
        line_dict = json.loads(line)
        tmp_today.update(line_dict)
        return tmp_today

    def close_file(self,file_name):
        tmp_today =json.dumps(self.stats_dict)
        self.stats.close()
        self.stats=open("/data/stats/"+file_name,"w")
        self.stats.write(tmp_today)
        self.stats.close()

    def action(self):
        pass




    def check_sql_status(self):
        try:
            self.database_use.ping()
            return True
        except Exception:
            return False

    def connect_mysql(self,file_name=None):
        if self.check_sql_status():
            pass
        else:
            self.database_use = pymysql.connect(host=Mysql.IP, user=Mysql.USER, password=Mysql.PASSWORD, database=Mysql.DATABASE)
        self.cursor = self.database_use.cursor()
        self.row_number = self.get_row_num()
        self.stats = open("/data/stats/" + file_name, "r")
        self.stats_dict = self.get_stats()




