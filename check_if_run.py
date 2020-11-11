import os
import psutil
import time
import json
from common.send_mail import Send_Mail

f=open("/data/pid/pid.txt","r")
today={}
line = f.read()
line_dict = json.loads(line)
today.update(line_dict)
f.close()

while True:
    pids=psutil.pids()
    if int(today["main.py"]) in pids:
        time.sleep(10*60)
    else:
        Send_Mail().send_error_mail()
        break

