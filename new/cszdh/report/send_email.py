import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

def send_mail(report_name, receiver ='yzclysmz@163.com'):
    '''
    发送测试报告到邮箱
    :param report_name: 需要发送的测试报告
    :param receiver: 邮件接收人S
    :return:
    '''
    # ----------------------------------------------------------
    # 获取邮件正文,读取测试报告的内容
    f = open(report_name, 'rb')
    mail_body = f.read()
    f.close()
    # 邮件服务器
    smtpserver = 'smtp.163.com'
    # 发件人和密码
    sender = 'yzclysmz@163.com'
    password = 'zy1229'
    # 接收人
    receiver = receiver
    # 邮件主题
    subject = u'智慧楼宇自动化测试报告'
    # ----------------------------------------------------------
    # 连接登录邮箱
    server = smtplib.SMTP(smtpserver, 25)
    server.login(sender, password)
    # ----------------------------------------------------------
    # 添加附件
    sendfile = open(report_name, 'rb').read()
    att = MIMEText(sendfile, "base64", 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    att['Content-Disposition'] = 'attachment;filename="result.html"'
    msg = MIMEMultipart('related')
    msgtext = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msgtext)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(att)
    # ----------------------------------------------------------
    # 发送邮件
    server.sendmail(sender, [receiver], msg.as_string())
    server.quit()
    print("发送成功!")

send_mail("result.html")