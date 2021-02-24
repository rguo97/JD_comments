import threading
import time
from ippool.get_ip import Get_Ip
from ippool.check_ip import Check_Ip
from common.constant import Mysql,Event_Name,Status
from common.send_mail import Send_Mail
from jd_commodity.commodity_id import Commodity_Id
from jd_commodity.commodity_comment import Commodity_Comment
from common.update_stats_file import Update_File
from common.event import Event
from concurrent.futures import ThreadPoolExecutor
from common.log import print_log
import json
import os
import random


def init_event():
    global tasks
    global commodity_page
    global commodity_list
    while True:
        FALG = False
        if tasks[0] == None:
            tasks[0] = Get_Ip(Mysql.DATABASE)
        if tasks[1] == None:
            tasks[1] = Check_Ip(Mysql.DATABASE)
        if tasks[2] == None:
            if commodity_page<40:
                commodity_page+=1
                #print_log("error","商品页码%s"%commodity_page)
                tasks[2] = Commodity_Id(Mysql.DATABASE, commodity_list[0],commodity_page)
            else:
                if len(commodity_list)>0:
                    commodity_list.pop(0)
                    commodity_page=1
                    tasks[2] = Commodity_Id(Mysql.DATABASE, commodity_list[0],commodity_page)
                else:
                    print_log("info","commodity_list is empty")
        if tasks[3] == None:
            tasks[3] = Commodity_Comment(Mysql.DATABASE)
        if tasks[4] == None:
            tasks[4] = Send_Mail()
        if tasks[5] == None:
            tasks[5] = Update_File()
        if FALG==False:
            print_log("info","No task need to init")
        time.sleep(20)


def add_event_produce():
    global event
    global tasks
    while True:
        if len(event[0])<3:
            event[0].append(Event(Event_Name.GETIP, tasks[0]))
            tasks[0]=None
        else:
            print_log("warning", "%s has existed" % Event_Name.GETIP)
        if len(event[1])<3:
            event[1].append(Event(Event_Name.CHECKIP, tasks[1]))
            tasks[1]=None
        else:
            print_log("warning", "%s has existed" % Event_Name.CHECKIP)
        if len(event[2])<3:
            event[2].append(Event(Event_Name.JDCOMMODITYID, tasks[2]))
            tasks[2]=None
        else:
            print_log("warning", "%s has existed" % Event_Name.JDCOMMODITYID)
        if len(event[3])<3:
            event[3].append(Event(Event_Name.JDCOMMODITYCOMMENT, tasks[3]))
            tasks[3]=None
        else:
            print_log("warning", "%s has existed" % Event_Name.JDCOMMODITYCOMMENT)
        if len(event[4]) < 1:
            event[4].append(Event(Event_Name.SENDEMAIL, tasks[4]))
            tasks[4]=None
        else:
            print_log("warning","%s has existed"%Event_Name.SENDEMAIL)
        if len(event[5]) < 1:
            event[5].append(Event(Event_Name.UPDATEFILE, tasks[5]))
            tasks[5]=None
        else:
            print_log("warning","%s has existed"%Event_Name.UPDATEFILE)

        time.sleep(60)
        

def delete_event_consumer():
    global event
    global thread_pool
    number=60
    while True:
        #print(tasks)
        local_time_hour = time.strftime("%H", time.localtime())
        local_time_minute = time.strftime("%M", time.localtime())
        local_time_second = time.strftime("%S", time.localtime())
        #random_time=str(random.randint(1,59))
        #print(event)
        if number==60:
            random_time=str(random.randint(1,59))
            number=0
        if event[5] == []:
            print_log("warning", "event list is empty")
        else:
            if (local_time_hour == "6" or local_time_hour == "10" or local_time_hour == "14" or \
                local_time_hour == "18" or local_time_hour == "22" or local_time_hour == "2") and \
                    local_time_minute == "10" and local_time_second == "30":
                thread_tasks[4] = (thread_pool.submit(event[4][0].action))
                event[4][0].update_status(Status.DOING, event[4][0].event_id)
            if local_time_hour == "23" and local_time_minute == "54" and local_time_second == "30":
                thread_tasks[5] = (thread_pool.submit(event[5][0].action))
                event[5][0].update_status(Status.DOING, event[5][0].event_id)
            if int(local_time_minute) % 5 == 0 and local_time_second == random_time:
                thread_tasks[1] = (thread_pool.submit(event[1][0].action))
                event[1][0].update_status(Status.DOING, event[1][0].event_id)
            if int(local_time_minute) % 5 == 0 and local_time_second == random_time:
            #if local_time_second == random_time:
                thread_tasks[3] = (thread_pool.submit(event[3][0].action))
                event[3][0].update_status(Status.DOING, event[3][0].event_id)
            if int(local_time_minute) % 10 == 0 and local_time_second == random_time:
            #if local_time_second == random_time:
                thread_tasks[0] = (thread_pool.submit(event[0][0].action))
                event[0][0].update_status(Status.DOING, event[0][0].event_id)
            if int(local_time_minute) % 10 == 0 and local_time_second ==  random_time:
                thread_tasks[2] = (thread_pool.submit(event[2][0].action))
                event[2][0].update_status(Status.DOING, event[2][0].event_id)

        number=number+1
        time.sleep(1)

def check_event():
    global thread_tasks
    global event
    time.sleep(5)
    while True:
        FLAG = False
        for i in range(len(thread_tasks)):
            if thread_tasks[i] != None:
                FLAG = True
                if thread_tasks[i].done():
                    event[i][0].update_status(Status.DONE, event[i][0].event_id)
                    thread_tasks[i]=None
                    event[i].pop(0)
                    
                    event[i][0].cursor.execute("select event_status from event where event_id='%s'"%str(event[i][0].event_id))
                    if event[i][0].cursor.fetchall()[0][0]==Status.DONE:
                        print_log("info","Event %s has ended"%str(event[i][0].event_id))
        if FLAG == False:
            print_log("warning","no event need to check")
        time.sleep(10)


pid_file_name="/data/pid/pid.txt"
f=open(pid_file_name,"r")
pid=os.getpid()
pid_dict={}
line = f.read()
line_dict = json.loads(line)
pid_dict.update(line_dict)
f.close()
pid_dict["main.py"]=pid

f=open(pid_file_name,"w")
f.write(json.dumps(pid_dict))
f.close()



event=[[],[],[],[],[],[],]
thread_tasks={0:None,1:None,2:None,3:None,4:None,5:None}
tasks={0:None,1:None,2:None,3:None,4:None,5:None}
commodity_page=1
commodity_list=["文胸","手环","笔记本电脑","内存条","平板电脑","拉杆箱","键盘","耳机","手机","手表","单反"]

thread_pool= ThreadPoolExecutor(max_workers=6)
threading.Thread(target=init_event).start()
threading.Thread(target=add_event_produce).start()
threading.Thread(target=delete_event_consumer).start()
threading.Thread(target=check_event).start()
#delete_event_consumer()
#threading.Thread(target=delete_event_consumer).start()


