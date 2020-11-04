import requests
from bs4 import BeautifulSoup
from common.constant import Mysql,Http_Head
from common.database import Database
from common.log import print_log
from common.random_ip import random_ip
import random


class IpPool(Database):

    def __init__(self,database):
        self.database =database

        super().__init__(self.database)

    def get_data(self):
        proxies=random_ip(self.select_all_date())
        try:
            url = "https://ip.ihuan.me/"
            page = requests.get(url, headers=Http_Head.headers,proxies=random.choice(proxies))
            soup = BeautifulSoup(page.text, "html.parser")
            soups = soup.find("tbody").find_all("tr")
        except Exception:
            print_log("error", "https://ip.ihuan.me can not reach")
            self.stats_dict["get_ip"][2] += 1
            url = "https://www.kuaidaili.com/free/"
            print_log("info","now use https://www.kuaidaili.com/free/ to get ip")
            try:
                page = requests.get(url, headers=Http_Head.headers,proxies=random.choice(proxies))
                soup = BeautifulSoup(page.text, "html.parser")
                soups = soup.find("tbody").find_all("tr")
            except Exception as e:
                print_log("error", "https://www.kuaidaili.com/free can not reach")
        finally:
            try:     
                ip_list = []
                for soup in soups:
                    ip_dict = {}
                    ip_dict["ip"] = soup.find_all("td")[0].text
                    ip_dict["port"] = soup.find_all("td")[1].text
                    ip_list.append(ip_dict)
                    self.stats_dict["get_ip"][1]+=1
                return ip_list
            except Exception as e:
                print_log("error", "get ip failed, because %s" % str(e))
                self.stats_dict["get_ip"][2] += 1
                self.get_data()

    def get_row_num(self):
        return self.cursor.execute("select * from ippool ") + 1

    def select_all_date(self):
        self.connect_mysql("get_ip_stats.txt")
        self.cursor.execute("select * from ippool where status=1")
        rows = self.cursor.fetchall()
        self.close_file("get_ip_stats.txt")
        return rows




