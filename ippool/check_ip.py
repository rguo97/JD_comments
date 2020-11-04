from .ip import IpPool
import time
from common.log import print_log
import os
from common.constant import Mysql
from common.event import Event

class Check_Ip(IpPool):
    def __init__(self,database):
        self.database = database
        super().__init__(self.database)

    def check_ip(self):
        self.stats_dict["check_ip"][0] += 1
        print_log("info", "IP check start")
        select_all_sql = "select id, ip from %s" % Mysql.IPPOOL
        self.cursor.execute(select_all_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            result = os.system("ping %s -w 5" % str(row[1])) == 0
            runtime = int(time.time())
            if (result == True):
                self.stats_dict["check_ip"][1] += 1
                self.cursor.execute("update ippool set status=1, update_time=%s where id='%s'" % (runtime,row[0]))
                print_log("info", "IP %s is working " % str(row[1]))
            else:
                self.stats_dict["check_ip"][2] += 1
                self.cursor.execute("update ippool set status=0, update_time=%s where id='%s'" % (runtime,row[0]))
                self.database_use.commit()
                print_log("warning", "ip %s has no effect" % str(row[1]))
        print_log("info", "IP check end")
        self.close_file("check_ip_stats.txt")

    def action(self):
        self.connect_mysql("check_ip_stats.txt")
        print(22222)
        print(self.database)
        self.check_ip()
        self.close_database()

class Check_Ip_Event(Event):
    def __init__(self, name,class_event):
        super().__init__(name,class_event)


