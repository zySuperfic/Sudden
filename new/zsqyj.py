import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time, traceback
try:
    from config import mail_user, mail_pass, sender, receivers, mail_host
except:
    raise("please create file and name is 'config.py', then reference comment setting each variable!")
"""
comment:
    mail_user, mail_pass, sender, receivers, mail_host is your personal data. so, I move it to a config.py and the file is ban to push github or gitlab or svn.
    mail_host = "smtp.163.com" set email.server. if your email is qq, replace 163 to qq.   # 设置服务器, 这个如果是qq, 就把163改成qq即可。
    mail_user = "XXXXXX@163.com"  # your email account or login name.
    mail_pass = "password"  # password, sometimes not set password, some email server need your client Authorization code(客户端授权码)
    sender = 'XXXXXX@163.com'   # 发送者 sender Email
    receivers = ['XXXXXX@163.com']  # receivers email，you can set more and use ',' to split.
"""
from functools import wraps
import logging
t = lambda:time.time()
# logging config, the more logging config information, you can learn from "https://www.cnblogs.com/yyds/p/6901864.html"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# this not config filename='my.log'.
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
# used to sendEmail
def sendEmail(message, subject):
    message = MIMEText(message, 'plain', 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())

"""
python decorator, send error email when catched error.
taskname: the email Title.
t() equal to time.time()
@wraps is used to save the function name and docstring. it's not necessary.
traceback.format_exc() is used to collect error message one by one.
the more decorator acknowledge you can search from google or baidu.
"""
def errorSendEmail(taskname):
    def functionwraper(function):
        @wraps(function)
        def wraper(*args, **kwargs):
            try:
                start_time = t()
                function(*args,**kwargs)
                end_time = t()
                logging.info("{} used {}s".format(function.__name__, end_time - start_time))
                sendEmail("succsess", taskname)
            except Exception as e:
                errorMessage = traceback.format_exc()
                logging.error(errorMessage)
                # sendEmail(errorMessage, taskname)
        return wraper
    return functionwraper


if __name__ == "__main__":
    @errorSendEmail("自动化测试信息")
    def testCount(l):
        a = [i for i in range(l)]
        # print(a)
        # print(1/0)
    testCount(1000000)

