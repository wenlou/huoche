# -*- coding: utf-8 -*-
"""
@author: sxj
"""
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from splinter.browser import Browser
from time import sleep
import traceback
# 用户名，密码
username = u""
passwd = u""
# 这是台州和济南的代码具体代码用f12工具查看
starts = u"%u53F0%u5DDE%2CTZH"
ends = u"%u6D4E%u5357%2CJNK"
# 时间格式2016-01-31
dtime = u"2017-02-01"
# 车次，选择第几趟，0则从上之下依次点击
order = 0
###乘客名
pa = u"沈晓健(学生)"
from_addr = 'sxj5203838@163.com'
password = 'a84884670'
to_addr = ['276372806@qq.com']
smtp_server = 'smtp.163.com'
"""网址"""
ticket_url = "https://kyfw.12306.cn/otn/leftTicket/init"
login_url = "https://kyfw.12306.cn/otn/login/init"
initmy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
def login():
    b.find_by_text(u"登录").click()
    sleep(3)
    b.fill("loginUserDTO.user_name", username)
    sleep(1)
    b.fill("userDTO.password", passwd)
    sleep(1)
    print u"等待验证码，自行输入..."
    while True:
        if b.url != initmy_url:
            sleep(1)
        else:
            break
def buy():
  try:
    while b.url == ticket_url:
        b.find_by_text(u"查询").click()
        sleep(1)
        try:
            if order != 0:
                b.find_by_text(u"预订")[order - 1].click()
            else:
                for i in b.find_by_text(u"预订"):
                    i.click()
        except:
            print u"还没开始预订"
            continue
  except:
      sleep(10)
      buy()
def huoche():
    global b
    b = Browser(driver_name="chrome")
    b.visit(ticket_url)
    while b.is_text_present(u"登录"):
        sleep(1)
        login()
        if b.url == initmy_url:
            break

    try:
        print u"购票页面..."
        # 跳回购票页面
        b.visit(ticket_url)
        # 加载查询信息
        b.cookies.add({"_jc_save_fromStation": starts})
        b.cookies.add({"_jc_save_toStation": ends})
        b.cookies.add({"_jc_save_fromDate": dtime})
        b.reload()
        sleep(2)
        if (pa.find(u"(学生)") != -1):
           if(b.url==ticket_url):
             b.find_by_text(u"学生").click()
        # 循环点击预订
        buy()
        sleep(1)
        b.find_by_text(pa).click()
        sendEmail()
        b.find_by_id("submitOrder_id").click()
        print  u"能做的都做了.....不再对浏览器进行任何操作"
    except Exception as e:
        print(traceback.print_exc())
# 编码转换方法
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
# 邮件方法
def sendEmail():
   msg = MIMEText('已经有余票赶快来购买！！！', 'plain', 'utf-8')
   msg['From'] = _format_addr('火车票 <%s>' % from_addr)
   msg['To'] = _format_addr('管理员 <%s>' % to_addr)
   msg['Subject'] = Header('火车票', 'utf-8').encode()
   server = smtplib.SMTP(smtp_server, 25)
   server.set_debuglevel(1)
   server.login(from_addr, password)
   server.sendmail(from_addr, [to_addr], msg.as_string())
   server.quit()

if __name__ == "__main__":
    huoche()