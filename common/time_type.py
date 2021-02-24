import time

def get_time():
    now = time.localtime()
    nowtime = str(now.tm_year)+"-"+str(now.tm_mon)+"-"+str(now.tm_mday)+"-"+str(now.tm_hour)+"-"+str(now.tm_min)+"-"+str(now.tm_sec)
    return nowtime

