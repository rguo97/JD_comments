from .ip import IpPool
import time
from common.log import print_log
from common.get_sql import get_insert_sql_ip,get_update_sql_ip
from common.event import Event


class Get_Ip(IpPool):
    def __init__(self,database):
        self.database=database
        super().__init__(database)

    def insert_data(self):
        self.stats_dict["get_ip"][0] += 1

        if self.row_number < 109:
            print_log("info", "Get ip start")
            ip_list = self.get_data()
            result = {}
            for i in range(len(ip_list)):
                result["id"] = i + self.row_number
                result["ip"] = ip_list[i]["ip"]
                result["port"] = ip_list[i]["port"]
                result["update_time"] = int(time.time())
                result["status"] = 1
                sql = get_insert_sql_ip(result)
                try:
                    self.cursor.execute(sql)
                    self.database_use.commit()
                    print_log("info", "IP %s has gotten" % str(result["ip"]))
                except Exception as e:
                    print_log("error", "%s" % str(e))
        else:
            print_log("info", "Update ip start")
            self.update_data()
            print_log("info", "Update ip end")
        self.close_file("get_ip_stats.txt")

    def update_data(self):
        self.stats_dict["update_ip"][0] += 1
        if (self.cursor.execute("select * from ippool where status='0'") > 0):
            rows = self.cursor.fetchall()
            ip_list = self.get_data()
            result = {}
            for row in rows:
                for ip in ip_list:
                    if ip["ip"] != row[0]:
                        result["id"] = row[4]
                        result["ip"] = ip["ip"]
                        result["port"] = ip["port"]
                        result["update_time"] = int(time.time())
                        result["status"] = 1

                        sql = get_update_sql_ip(result)
                        try:
                            self.stats_dict["update_ip"][1] += 1
                            self.cursor.execute(sql)
                            self.database_use.commit()
                            print_log("info", "IP %s has updated" % str(result["ip"]))
                        except Exception as e:
                            self.stats_dict["update_ip"][2] += 1
                            print_log("error", "%s" % str(e))
        else:
            print_log("info", "No IP need to update")

    def action(self):
        self.connect_mysql("get_ip_stats.txt")
        self.insert_data()
        self.close_database()

class Get_Ip_Event(Event):
    def __init__(self, name, class_event):
        super().__init__(name, class_event)

