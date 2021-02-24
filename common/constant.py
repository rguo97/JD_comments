from .random_ip import random_chrome,random_apple
#logging
class Logging:
    LOG_LEVEL = ["ERROR", "INFO", "WORNING", ]
    LOG_INCLUDE = ["ippool",]


#mysql
class Mysql:
    IP = "localhost"
    USER = "root"
    DATABASE = "spider"
    PASSWORD = "******"

    IPPOOL = "ippool"
    COMMODITY = "commodity"
    COMMODITY_ID = "commodity_id"
    COMMENTS_COMMENTS = "comments"

    EVENT = "event"
    IPSITE = "ipsite"



#header
class Http_Head:
    headers = {
        'Accept': "*/*",
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Connection': "keep-alive",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/%s.36 (KHTML, like Gecko) Chrome/67.0.%s.79 Safari/%s.36"%(random_apple(),random_chrome(),random_apple()),

    }

#mail
class SELF_Email:
    MAIL_HOST = "smtp.163.com"
    MAIL_SENDER = "xxxxx@163.com"
    MAIL_LICENSE = "*****"
    MAIL_RECEIVER = "xxxxx@163.com"

    FROM_WHICH = "我的服务器<xxxxxx@163.com>"
    TO_WHICH = "rguo<xxxxx@163.com>"
    SUBJECT = " 服务器运行情况汇总"
    WRONG_SUBJECT = "main.py 运行出现问题"


#status
class Status:
    NOTDO = "2"
    DOING = "1"
    DONE = "0"




class Event_Name:
    CHECKIPSITE = "检查IP来源网站"
    GETIP="获取IP"
    CHECKIP="检查IP"
    JDCOMMODITYID="获取京东商品编号"
    JDCOMMODITYCOMMENT = "获取京东商品评论"
    SENDEMAIL="给手机发送邮件"
    UPDATEFILE="更新记录文件"
    EXPORTEVENT="导出事件"

Jd_Commodity_Dict={
    "文胸": 1,
    "手环": 2,
    "笔记本电脑": 3,
    "内存条": 4,
    "平板电脑": 5,
    "拉杆箱": 6,
    "键盘": 7,
    "耳机": 8,
    "手机": 9,
    "手表": 10,
}

