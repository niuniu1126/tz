import tushare
import pandas
import time
import smtplib
from email.mime.text import MIMEText


# 股票类
class Share(object):

    def __init__(self, code, buy, sale):
        self.code = code
        self.name = None  # 公司名字
        self.openn = None  # 开盘价
        self.pre_close = None  # 昨日收盘价
        self.price = None  # 实时价格
        self.high = None  # 最高
        self.low = None  # 最低
        self.change = None  # 涨幅

        self.buy = buy  # 买点或止损点
        self.sale = sale  # 止盈点


# 邮件发送的方法  需要下载安装pyemail模块
def sendMail(subject, content):
    msg_from = 'XXXXX@163.com'  # 发送方邮箱
    passwd = 'XXXXX'  # 授权码
    msg_to = 'XXXXX@qq.com'  # 收件人邮箱

    mailServer = "smtp.163.com"  # 邮件服务器
    port = 465  # 端口号

    # 构造邮件部分
    msg = MIMEText(content)  # 把正文添加到邮件
    msg['Subject'] = subject  # 把主题添加到邮件
    msg['From'] = msg_from  # 把发送人添加到邮件
    msg['To'] = msg_to  # 把接收人添加到邮件

    # 发送邮件代码
    try:
        s = smtplib.SMTP_SSL(mailServer, port)
        s.login(msg_from, passwd)  # 客户端登录发送人邮箱
        s.sendmail(msg_from, msg_to, msg.as_string())  # 发送邮件
        print("发送成功")
    except Exception as e:
        print(e)
        print("发送失败")
    finally:
        print("结束！")
        s.quit()


# 获取股票行情数据的方法
def getData(shareList):
    for share in shareList:

        data = tushare.get_realtime_quotes(share.code)
        print(data)
        # 给传进来的股票对象的属性赋值
        share.name = data.loc[0][0]  # 公司名字
        share.openn = float(data.loc[0][1])  # 开盘价
        share.pre_close = float(data.loc[0][2])  # 昨日收盘价
        share.price = float(data.loc[0][3])  # 实时价格
        share.high = float(data.loc[0][4])  # 最高
        share.low = float(data.loc[0][5])  # 最低
        share.change = round((share.price - share.pre_close) / share.pre_close * 100, 2)  # 涨幅

        dis = "股票名：" + share.name + " 价格：" + str(share.price) + " 涨幅：\
            " + str(share.change) + "%" + " 开：" + str(share.openn) + " 昨收：\
            " + str(share.pre_close) + " 高：" + str(share.high) + " 低：" + str(share.low)

        print(dis)

        msg = "投资建议：不做任何操作！"
        if share.price >= share.sale:
            msg = "达到止盈点" + str(share.sale) + "，当前价格" + str(share.price) + "，建议卖出！"
            subject = "注意！价格破位！"
            print("准备发送邮件...")
            # sendMail(subject, msg)  # 股票价格破位时发送邮件

        elif share.price <= share.buy:
            msg = "达到止损或买入点" + str(share.buy) + "，当前价格" + str(share.price) + "，建议买入或者止损！"
            subject = "注意！价格破位！"
            print("准备发送邮件...")
            # sendMail(subject, msg)  # 股票价格破位时发送邮件
        print(msg)


# 主逻辑
while 1 == 1:
    share1 = Share("000425", 5.05, 5.50)
    # share2 = Share("000006", 13.6, 13.7)
    # share3 = Share("000591", 13.6, 13.7)

    # sssList = [share1, share2, share3]
    sssList = [share1]

    getData(sssList)  # 股票对象作为参数传入函数

    time.sleep(60)
