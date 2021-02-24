import requests
from common.constant import Http_Head, Mysql,Status
from ippool.ip import IpPool
from common.random_ip import random_ip
import random
import json
import time
from common.log import print_log
from .jd import Jd
from common.get_sql import get_insert_sql_comment
from .commodity_id import Commodity_Id
from common.event import Event


class Commodity_Comment(Jd):

    def __init__(self,database):

        super().__init__(database)



    def get_commodity_id(self):
        try:
            sql="select commodity_id from commodity_id where commodity_status=2 limit 1"
            self.cursor.execute(sql)
            commodity_id = self.cursor.fetchall()[0][0]
            return commodity_id
        except Exception as e:
            print(e)

    def get_comment(self,commodity_id,page):

        url = self.get_commodity_comment_url(commodity_id,page)
        proxies = random_ip(IpPool(Mysql.DATABASE).select_all_date())
        try:
            self.stats_dict["get_jd_comment"][0] += 1
            p=random.choice(proxies)
            page_text = requests.get(url, headers=Http_Head.headers, proxies=p)
            print_log("info", "jd comment %s page %s get successfully" % (commodity_id, page))
        except Exception as e:
            self.stats_dict["get_jd_comment"][2] += 1
            print_log("error", "jd comment %s page %s get Failed,because %s" % (commodity_id, page, str(e)))
        page_str = page_text.text[20:-2]
        page_dict = json.loads(page_str)
        comments_lists = page_dict["comments"]
        return comments_lists


    def insert_data(self):
        result={}
        self.commodity_id = self.get_commodity_id()
        result["commodity_id"]=self.commodity_id
        result["commodity_status"]=Status.DOING
        Commodity_Id(Mysql.DATABASE).update_data(result)
        for page in range(60):
            comments_lists = self.get_comment(self.commodity_id,page)
            for comments_list in comments_lists:
                result["commodity_name"] = 1
                result["commodity_id"] = self.commodity_id
                result["user_id"] = comments_list["id"]
                result["comments"] = comments_list["content"]
                result["size"] = comments_list["productSize"]
                sql = get_insert_sql_comment(result)
                try:

                    self.stats_dict["get_jd_comment"][1] += 1
                    self.cursor.execute(sql)
                    self.database_use.commit()
                except Exception as e:
                    print_log("error", "jd comment insert Failed,because %s"%str(e))
            time.sleep(1)
        result["status"] = Status.DONE
        Commodity_Id(Mysql.DATABASE).update_data(result)
        self.close_file("get_commodity_comments.txt")
        time.sleep(5)

    def get_row_num(self):
        return self.cursor.execute("select * from comments ")+1


    def get_commodity_comment_url(self,commodity_id,page):
        tmp_url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1"%(commodity_id,str(page+1))
        return tmp_url


    def action(self):
        self.connect_mysql("get_commodity_comments.txt")
        self.insert_data()
        self.close_database()

class Get_Commont_Event(Event):
    def __init__(self,name,class_event):
        super().__init__(name,class_event)

