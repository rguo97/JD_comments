import time
import os
from common.constant import Logging


class Log():

    def __init__(self, level=None, message=None):
        self.get_time()
        self.get_thread()
        self.get_product()
        self.get_level(level=level)
        self.get_message(message=message)

    def write_log(self):
        f = open("/data/log/" + self.product + ".log", "a")
        f.write(self.time + "  " + self.thread_id + "  " + self.product + "  " + self.level + "  " + self.message + "\n")
        f.close()

    def get_time(self):
        self.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def get_thread(self):
        import threading
        self.thread_id = "Thread-" + str(threading.currentThread().ident)

    def get_product(self):
        path = os.getcwd()
        self.product = path.split('/')[-1]

        if self.product in Logging.LOG_INCLUDE:
            self.product = self.product

        else:
            self.product = "daily"

    def get_level(self, level):
        self.level = level.upper()

    def get_message(self, message):
        self.message = message

def print_log(level, message):
    log = Log(level=level, message=message)
    log.write_log()
