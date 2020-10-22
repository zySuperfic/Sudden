# coding=utf-8
from new.yanzi_jiekou.common.operate_excel import *
# from common.operate_excel import *
import unittest
from parameterized import parameterized
import requests
from new.yanzi_jiekou.common.send_request import RunMethod
import json
from new.yanzi_jiekou.common.logger import MyLogging
import jsonpath
from new.yanzi_jiekou.common.is_instance import IsInstance
from new.yanzi_jiekou.common.HTMLTestRunner import HTMLTestRunner
import os
import time

lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
file_path = lib_path + "/" + "接口自动化测试.xlsx"  # excel的地址
# file_path = "D:\qycache\接口自动化测试.xlsx"
sheet_name = "工作表1"
log = MyLogging().logger


def getExcelData():
    list = ExcelData(file_path, sheet_name).readExcel()
    return list
# print(getExcelData())

# 打印登录返回token必填值
# def login():
#     url = "http://v4.demo.qiyebox.com/auth/oauth/token?username=yanzi&pCode=R5eGR5f0xc5sJ5VeZIBxtg%3D%3D&randomStr=75461594192181112&code=6666&grant_type=password&scope=server"
#     headers = {
#         "Content-Type": "application/json;charset=UTF-8",
#         "Authorization": "Basic cGlnOnBpZw=="
#     }
#     r = requests.get(url=url, headers=headers)
#     return r.json()['access_token']
# # print("bearer "+login())

class TestCase(unittest.TestCase):

    @parameterized.expand(getExcelData())
    def test_api(self, rowNumber, caseRowNumber, testCaseName, priority, apiName, url, method, parmsType, data,
                 checkPoint, isRun, result):
        if isRun == "Y" or isRun == "y":
            log.info("【开始执行测试用例：{}】".format(testCaseName))
            headers = {"Content-Type": "application/json"}
            data = json.loads(data)  # 字典对象转换为json字符串
            c = checkPoint.split(",")
            log.info("用例设置检查点：%s" % c)
            print("用例设置检查点：%s" % c)
            log.info("请求url：%s" % url)
            log.info("请求参数：%s" % data)
            r = RunMethod()
            res = r.run_method(method, url, data, headers)
            log.info("返回结果：%s" % res)

            flag = None
            for i in range(0, len(c)):
                checkPoint_dict = {}
                checkPoint_dict[c[i].split('=')[0]] = c[i].split('=')[1]
                # jsonpath方式获取检查点对应的返回数据
                list = jsonpath.jsonpath(res, c[i].split('=')[0])
                value = list[0]
                check = checkPoint_dict[c[i].split('=')[0]]
                log.info("检查点数据{}：{},返回数据：{}".format(i + 1, check, value))
                print("检查点数据{}：{},返回数据：{}".format(i + 1, check, value))
                # 判断检查点数据是否与返回的数据一致
                flag = IsInstance().get_instance(value, check)

            if flag:
                log.info("【测试结果：通过】")
                ExcelData(file_path, sheet_name).write(rowNumber + 1, 12, "Pass")
            else:
                log.info("【测试结果：失败】")
                ExcelData(file_path, sheet_name).write(rowNumber + 1, 12, "Fail")

            # 断言
            self.assertTrue(flag, msg="检查点数据与实际返回数据不一致")
        else:
            unittest.skip("不执行")



if __name__ == '__main__':
    # unittest.main()
    # Alt+Shift+f10 执行生成报告

    # 报告样式1
    suite = unittest.TestSuite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    report_path = r"C:\Users\Administrator\PycharmProjects\xin\new\yanzi_jiekou\report\report.html"
    with open(report_path, "wb") as f:
        runner = HTMLTestRunner(stream=f, title="Esearch接口测试报告", description="测试用例执行情况", verbosity=2)
        runner.run(suite)

# test_case.py