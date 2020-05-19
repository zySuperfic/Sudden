# coding:utf-8;
# HTMLTemp
import unittest
from unittest.test.testmock.testpatch import function
from HTMLTestRunner_cn import HTMLTestRunner
import requests
import json
import xlrd
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time, traceback

ErrorCount = 0
TotalCount = 0
errorMessage = []

try:
    from config import mail_user, mail_pass, sender, receivers, mail_host
except:
    raise ("please create file and name is 'config.py', then reference comment setting each variable!")

from functools import wraps
import logging

t = lambda: time.time()
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


def errorSendEmail(taskname):
    def functionwraper(function):
        @wraps(function)
        def wraper(*args, **kwargs):
            try:
                start_time = t()
                function(*args, **kwargs)
                end_time = t()
                logging.info("{} used {}s".format(function.__name__, end_time - start_time))
                # sendEmail("succsess", taskname)
            except Exception as e:
                errorMessage = traceback.format_exc()
                logging.error(errorMessage)
                sendEmail(errorMessage, taskname)

        return wraper

    return functionwraper


url = "http://v4.demo.qiyebox.com/bills/BuildBill/buildBill"

headers = {
    'Authorization': "Bearer 430b408b-7c93-4e56-bd6b-3a25089d1e80",
    'Content-Type': "application/json;charset=UTF-8",
}


# 查询前准备, 整理成data.向服务器请求数据
def queryData(test_data):
    # for i in test_data:
    # data[i] = test_data[i]
    # print(data, "after Data")
    # print(data["leaseTermRange"], data['contractCostList'], data['areaRent'])
    # print(test_data['sendDataList'])
    return json.dumps(test_data['sendDataList']).replace("None", "null")


# 发起请求，拿到数据
def getJsonData(queryData):
    r = requests.post(url, headers=headers, data=queryData.encode("utf-8"))
    # print(r.text, "getJsonData")
    serverData = r.json()['data']

    if serverData:
        return serverData
    else:
        return False


# 请求完成后，处理数据
def processData(serverData):
    # print(serverData['code'])
    # print(serverData, "12222")
    # timePriceList = serverData['leaseResourceList'][0]['contractCostList'][0]['timePriceList']
    timePriceList = serverData['resource'][0]['details'][0]['costDetails']
    TotalMoney = round(sum(i['money'] for i in timePriceList), 2)
    return TotalMoney


# excel读取数据
# @errorSendEmail
def excelGetData():
    path = "D:\pyceshi\ceshi\case.xlsx"
    # path = "E:\shiyan\ceshi\case\case.xlsx"
    book = xlrd.open_workbook(path)
    sheet1 = book.sheets()[0]

    nrows = sheet1.nrows
    # print(nrows)
    # ncols = sheet1.ncols
    # print(ncols)
    resultData = []
    title = sheet1.row_values(0)
    for i in range(1, 188):  # 1,2,3
        row1_values = sheet1.row_values(i)
        OneLineDict = {}
        for key, value in zip(title, row1_values):
            if isinstance(value, str):
                value = value.replace("\n", "").replace("，", ",").replace(" ", "")
            if key == "sendDataList":
                OneLineDict[key] = eval(value)
            else:
                OneLineDict[key] = value
        resultData.append(OneLineDict)
    return resultData


# excel 处理数据
# def excelProcessData():
#     pass

if __name__ == "__main__":
    resultData = excelGetData()
    # print("bbbbbbbbbbb")
    # print(resultData)
    # xlsd, 读取每行的数据，传入queryData中。
    # rowData = excelGetData()s
    # resultData = excelProcessData(rowData)

    test = unittest.TestSuite()
    for eachLine in resultData:
        testCaseTotalMoney = eachLine.pop("totalmoney")
        #testCaseTotalMoney1 = eachLine.pop("totalmoney1")
        # print(eachLine, "1111")
        data = queryData(eachLine)
        # print(data, "kkkkkkk")

        serverData = getJsonData(data)
        TotalCount += 1
        if serverData:
            # print(serverData, "llllllllllllllllllllllll")
            TotalMoney = processData(serverData)
            print(testCaseTotalMoney,TotalMoney)
            # num = 0

            if testCaseTotalMoney == TotalMoney or testCaseTotalMoney1 == TotalMoney:
                # print("case_money: ", testCaseTotalMoney, "     ", "res_money: ", TotalMoney,
                #   "             result：   pass  ", "等级： P1")
                pass
            else:
                ErrorCount += 1
                errorMessage.append(data)
                # errorMessage.append(serverData)
                # print("case_money: ", testCaseTotalMoney, "     ", "res_money: ", TotalMoney,
                #   "             result：   false  ", "等级： P1")

            # testcase 从test_data中获取
            # testcase = dict(totalmoney=218.38)
            # assert testCaseTotalMoney == TotalMoney
        else:
            print("获取数据失败")

    r = "error count is {} , total_count is {} and right_count is {}".format(ErrorCount, TotalCount,
                                                                             TotalCount - ErrorCount)
    print("error count is {} , total_count is {} and right_count is {}".format(ErrorCount, TotalCount,
                                                                               TotalCount - ErrorCount))
    res = []
    for i in errorMessage:
        res.append(json.dumps(i))
    res = "\n\n\n".join(res)
    # print(res)
    sendEmail("运行结果：" + r + '\n\n' + '错误用例参数：' + res, "error Case")

    # def set_func(func):
    #     num = 0   # 闭包中外函数中的变量指向的引用不可变
    #     def call_func():
    #         func()
    #         if serverData['code' = 0]:
    #             nonlocal num # 使用nonlocal 访问修改外部函数变量
    #             num += 1
    #             print("false",num)
    #             return num
    #         else:
    #             print("sucess",num)
    #     return call_func

    # @errorSendEmail("自动化测试信息")
    # def testCount(l):
    #     a = [i for i in range(l)]
    #     # print(a)
    #     # print(1/0)
    # testCount(1000000)

# class Test(unittest.unitcase):
#     def setUpClass(self):
#         pass
#     def tearDownClass(self):
#         pass
#     def setUp(self):
#         self.driver=webdriver.chrome()
# def tearDown(self):
# slef.deiver.quit()
# #获取标题
# def test_getTitle(self):
# url='http://www.baidu.com'
# self.driver.get(url)
# title=self.driver.title
# print(' 当前网页的titlt为:',title)
# self.assertEqual(title,'百度一下，你就知道;,'页面TITLE错误')

# if __init__=='__name__':
# unittest.main()
# #或者
# if __init__=='__main__':
# suite=unittest.suite()
# suite.addTests(unittest.TestLoad().loadTestSFromTestCase(TestClass)
# with open(filename,'wb') as fp:
# runner=HTMLTestRunner(stream=fp,title='标题', description='测试用例')
# runner.run(suite)