import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from .constant import SELF_Email
from .log import print_log
import json
import pymysql
import os
from common.update_stats_file import Update_File



class Send_Mail():

    def send_mail(self):
        print_log("info", "Start to send email")
        blog_stats={}
        
        Update_File().add_file()
        #cursor=database.cursor()
        #blog_stats["user_online"] = cursor.execute("select * from wp_statistics_useronline")
        #blog_stats["today_visitor"] = cursor.execute("select * from wp_statistics_visitor where last_counter='%s'"%time.strftime(("%Y_%m_%d)"),time.localtime()))
        #cursor.execute("select ip from wp_statistics_visitor ORDER BY ID DESC limit 3")
        #blog_stats["lastest_visitor"] = cursor.fetchall()
        #cursor.execute("select visit from wp_statistics_visit where last_counter='%s'"%time.strftime(("%Y_%m_%d)"),time.localtime()))
        #blog_stats["today_click"] = cursor.fetchall()[0]
        #database.close()

        blog_stats["user_online"] =20
        blog_stats["today_visitor"] = 15
        blog_stats["lastest_visitor"] = 10
        blog_stats["today_click"] = 5
        mail = MIMEMultipart("related")

        mail_subject = str(time.strftime(("%Y-%m-%d %H:%M:%S"), time.localtime())) + SELF_Email.SUBJECT

        today = {}
        f = open("/data/stats/daily_stats.txt", "r")
        line = f.read()
        line_dict = json.loads(line)
        today.update(line_dict)
        mail_body = "你好:"+"<br>" +"<br>"+ "&emsp&emsp今日服务器运行情况已送达，请注意查收 :)"+"<br>"
        mail_table = "爬虫情况"+'<br>'+'''
        <br>
        <table border=1>
        <tr><th>模块</th><th>运行次数</th><th>获取数量</th><th>失败次数</th></tr>
        <tr><th>获取IP</th><th>%s</th><th>%s</th><th>%s</th></tr>
        <tr><th>检查IP</th><th>%s</th><th>%s</th><th>%s</th></tr>
        <tr><th>更新IP</th><th>%s</th><th>%s</th><th>%s</th></tr>
        <tr><th>获取JD商品ID</th><th>%s</th><th>%s</th><th>%s</th></tr>
        <tr><th>获取JD商品comment</th><th>%s</th><th>%s</th><th>%s</th></tr>
        </table>
        <br>
        </br>
        ''' % (today["get_ip"][0], today["get_ip"][1], today["get_ip"][2],
               today["check_ip"][0], today["check_ip"][1], today["check_ip"][2],
               today["update_ip"][0], today["update_ip"][1], today["update_ip"][2],
               today["get_jd_id"][0], today["get_jd_id"][1], today["get_jd_id"][2],
               today["get_jd_comment"][0], today["get_jd_comment"][1], today["get_jd_comment"][2])



        table2_text = '<br>'+"博客访问情况"+'<br>'+\
            '''
            <br>
            <table border=1>
            <tr><th>目前今日访客</th><th>%s</th></tr>
            <tr><th>目前今日点击量</th><th>%s</th></tr>
            <tr><th>最近访客</th><th>%s</th><th>%s</th><th>%s</th></tr>
            <tr><th>当前在线</th><th>%s</th></tr>
            </table>''' \
            % (blog_stats["today_visitor"], blog_stats["today_click"], blog_stats["lastest_visitor"], blog_stats["lastest_visitor"], blog_stats["lastest_visitor"], blog_stats["user_online"], )




        mail_body = mail_body + mail_table + "<br>" + "&emsp&emsp每天都要开心哦！\n"



        mail["From"] = SELF_Email.FROM_WHICH
        mail["To"] = SELF_Email.TO_WHICH
        mail["Subject"] = Header(mail_subject, 'utf-8')
        message_text = MIMEText(mail_body, "html")
        message_text2 = MIMEText(table2_text, "html")
        handle_file("daily")
        File = '/data/email/log.doc'
        att1 = MIMEText(open(File, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'

        att1.add_header('Content-Disposition', 'attachment', filename="log.doc")


        mail.attach(message_text)
        mail.attach(message_text2)
        mail.attach(att1)

        try:
            email = smtplib.SMTP()
            email.connect(SELF_Email.MAIL_HOST, 25)
            email.login(SELF_Email.MAIL_SENDER, SELF_Email.MAIL_LICENSE)
            email.sendmail(SELF_Email.MAIL_SENDER, SELF_Email.MAIL_RECEIVER, mail.as_string())
            print_log("info", "Email send success")
        except Exception as e:
            print_log("error", "Email send fail")
    def action(self):
        self.send_mail()

    def send_error_mail(self):
        print_log("info", "There is something wrong")
        mail = MIMEMultipart("related")
        mail_subject = str(time.strftime(("%Y-%m-%d %H:%M:%S"), time.localtime())) + SELF_Email.WRONG_SUBJECT
        mail_body="main.py 停止运行，请及时查看，具体信息查看附件"
        mail["From"] = SELF_Email.FROM_WHICH
        mail["To"] = SELF_Email.TO_WHICH
        mail["Subject"] = Header(mail_subject, 'utf-8')
        message_text = MIMEText(mail_body,"plain","utf-8")
        handle_file("wrong")
        File = '/data/email/log.doc'
        att1 = MIMEText(open(File, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1.add_header('Content-Disposition', 'attachment', filename="log.doc")
        mail.attach(message_text)
        mail.attach(att1)
        try:
            email = smtplib.SMTP()
            email.connect(SELF_Email.MAIL_HOST, 25)
            email.login(SELF_Email.MAIL_SENDER, SELF_Email.MAIL_LICENSE)
            email.sendmail(SELF_Email.MAIL_SENDER, SELF_Email.MAIL_RECEIVER, mail.as_string())
            print_log("info", "Email send success")
        except Exception as e:
            print_log("error", "Email send fail")


def handle_file(level):
    if level=="daily":
        os.system("cat /data/log/daily.log |grep 'ERROR'> /data/email/log.doc")
        os.system("cat /data/log/daily.log |grep 'no effect'>> /data/email/log.doc")
    elif level=="wrong":
        os.system("cat /data/log/daily.log |grep 'ERROR'> /data/email/log.doc")
        os.system("cat /data/log/daily.log |grep 'WARNING'>> /data/email/log.doc")
