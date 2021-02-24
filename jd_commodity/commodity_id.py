import requests
from bs4 import BeautifulSoup
from common.constant import Http_Head, Mysql,Status, Jd_Commodity_Dict
from ippool.ip import IpPool
from common.random_ip import random_ip
import random
import urllib.parse
from common.log import print_log
from .jd import Jd
from common.get_sql import get_update_sql_commodity,get_insert_sql_commodity
from common.event import Event

class Commodity_Id(Jd):
    def __init__(self,database, commodity=None,page=None):
        if commodity ==None:
            pass
        else:
            self.commodity = commodity
            self.commodity_utf = urllib.parse.quote(self.commodity)
        self.page = page
        super().__init__(database)

    def get_commodity_id(self):
        proxies = random_ip(IpPool(Mysql.DATABASE).select_all_date())
        url = self.get_commodity_id_url(self.page)
        print_log("error","爬取京东商品ID的url%s"%str(url))
        try:
            self.stats_dict["get_jd_id"][0] += 1
            page_text = requests.get(url, headers=Http_Head.headers, proxies=random.choice(proxies))
            soup = BeautifulSoup(page_text.text, "html.parser")
            shopping_ids = str(soup.find_all("script")[3]).split("wids:'")[1].split("',uuid")[0].split(",")
            print_log("info", "jd commodity %s page %s get successfully" % (str(self.commodity),self.page))
        except Exception as e:
            self.stats_dict["get_jd_id"][2] += 1
            print_log("error", "jd commodity %s page %s get failed, because %s" % (str(self.commodity),self.page, str(e)))
        return shopping_ids

    def insert_data(self):

        result = {}
        shopping_ids = self.get_commodity_id()
        shopping_ids.pop(0)
        for shopping_id in shopping_ids:
            result["commodity_id"] = str(shopping_id)
            result["commodity_name"] = self.commodity
            result["commodity_status"] = 2
            sql = get_insert_sql_commodity(result)
            try:
                self.stats_dict["get_jd_id"][1] += 1
                self.cursor.execute(sql)
                self.database_use.commit()
                print_log("info","JD_commodity %s %s insert successfully" % (str(self.commodity), result["commodity_id"]))
            except Exception as e:
                print_log("error", "jd commdity %s %s insert failed, because %s" % (
                    str(self.commodity), str(result["commodity_id"]), str(e)))
        self.close_file("get_commodity_id.txt")


    def update_data(self,result={}):
        self.connect_mysql("get_commodity_id.txt")
        sql=get_update_sql_commodity(result)
       
        try:
            #self.stats_dict["check_id"][1]+=1
            print(sql)
            self.cursor.execute(sql)
            self.database_use.commit()
            if result["commodity_status"]==Status.DONE:
                print_log("info","JD_ID %s has gotton"%str(result["commodity_id"]))
            elif result["commodity_status"]==Status.DOING:
                print_log("info","JD_ID %s is getting"%str(result["commodity_id"]))
            elif result["commodity_status"]==Status.NOTDO:
                print_log("info","JD_ID %s will be gotton later"%str(result["commodity_id"]))
        except Exception as e:
            #self.stats_dict["checkid"][2] += 1
            print_log("error", "jd commodity id %s update Failed, because %s" % (str(result["commodity_id"]),str(e)))
        finally:
            self.close_file("get_commodity_id.txt")


    def get_commodity_id_url(self, page):
        tmp_url = "https://search.jd.com/Search?keyword=%s&wq=%s&page=%s&s=%s&click=0" % (self.commodity_utf,self.commodity_utf, str(page),str(1+(page-1)*25))
        return tmp_url

    def action(self):
        self.connect_mysql("get_commodity_id.txt")
        self.insert_data()
        self.close_database()


