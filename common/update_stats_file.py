import json
from .log import print_log
import os


class Update_File():

    def update_file(self):
        pass
        try:
            file_path = "/data/stats/"
            file_list = os.listdir(file_path)
            tmp_today = {}
            for file_name in file_list:
                f = open(file_path+file_name, "r")
                line = f.read()
                line_dict = json.loads(line)
                tmp_today.update(line_dict)
                zero = [0, 0, 0]
                for key in tmp_today:
                    tmp_today[key] = zero
                f.close()
                f = open(file_path+file_name, "w")
                f.write(json.dumps(tmp_today))
                f.close()
                print_log("info","%s has been updated"%file_name)
        except Exception as e:
            print_log("error","%s update failed, because %s"%(file_name,str(e)))

        try:
            os.system("sudo rm /usr/local/lib/python3.8/dist-packages/VESA-3.8-project/nohup.out")
            print_log("info","nohup.out has been deleted")
        except Exception as e:
            print_log("error","nohuo.out delete failed, because %s"%str(e))
    
    def action(self):
        self.update_file()

    def add_file(self):
        try:
            file_path = "/data/stats/"
            file_list = os.listdir(file_path)
            file_list.remove("daily_stats.txt")
            tmp_today = {}
            for file_name in file_list:
                f = open(file_path + file_name, "r")
                line = f.read()
                line_dict = json.loads(line)
                tmp_today.update(line_dict)
                f.close()
            f = open("/data/stats/daily_stats.txt", "w")
            f.write(json.dumps(tmp_today))
            f.close()
            print_log("info", "daily_stats.txt has been updated")
        except Exception as e:
            print_log("error", "daily_stats.txt update failed, because %s" % str(e))


