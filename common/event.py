from .constant import Status,Mysql
import pymysql
#import time
from .time_type import get_time
from .log import print_log
import threading



class Event():
    def __init__(self,name,class_event):
        self.database_use = pymysql.connect(host=Mysql.IP, user=Mysql.USER, password=Mysql.PASSWORD, database=Mysql.DATABASE)
        self.cursor=self.database_use.cursor()
        self.lock = threading.RLock()
        self.event_id = self.auto_event_id()
        self.event_name = name
        print_log("info","Event %s has been created now"%self.event_name)
        self.event_status = Status.NOTDO
        self.create_time = get_time()
        self.class_event = class_event
        self.display = 1
        self.run()


    def run(self):
        self.finish_time=get_time()
        self.insert_data()


    def insert_data(self):
        try:
            self.cursor.execute("insert into event(event_id,event_name,create_time,finish_time,event_status,display)"\
                            "values ('%s','%s','%s','%s','%s','%s')"\
                            %(self.event_id,self.event_name,self.create_time,self.finish_time,self.event_status,self.display)
                            )
            self.database_use.commit()
            print_log("info","Event %s %s insert successfully" % (str(self.event_id),str(self.event_name)))
        except Exception as e:
            print_log("error","Event %s %s insert faild" % (str(self.event_id),str(self.event_name)))

    def update_status(self,status,event_id):
        runtime=get_time()
        self.connect_mysql()
        self.cursor.execute("update event set event_status=%s,finish_time=%s where event_id=%s"%(status,runtime,event_id))
        self.database_use.commit()

    def action(self):
        self.class_event.action()

    def auto_event_id(self):
        self.lock.acquire()
        try:
            return self.cursor.execute("select * from event") + 1
        finally:
            self.lock.release()

    def export_data(self):
        pass

    def check_sql_status(self):
        try:
            self.database_use.ping()
            return True
        except Exception:
            return False

    def connect_mysql(self):
        if self.check_sql_status():
            pass
        else:
            self.database_use = pymysql.connect(host=Mysql.IP, user=Mysql.USER, password=Mysql.PASSWORD, database=Mysql.DATABASE)


