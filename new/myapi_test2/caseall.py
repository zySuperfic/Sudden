#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-03 10:07
import unittest
from HTMLTestRunner_cn import HTMLTestRunner
import time
import tool
import json


class Test(unittest.TestCase):
    heixiongjing = 123
    # 获取测试数据

def demo(i):
    def case(self):
        CaseUrl = i[2]+i[3]
        RequestType = i[4]
        Paramete = i[5]
        Result = json.loads(i[6])
        apiresult = apitest.request(RequestType, CaseUrl, Paramete, '')
        code = apiresult.status_code
        assert code == 200, '▇▇▇请求失败！'+'  '+'code:'+str(code)+'  '+'url='+CaseUrl
        pam = json.loads(apiresult.text)
        apitest.Assert(pam, Result)

    setattr(case, '__doc__', str(i[1]))
    return case

def testall(num):
    for i in num:
        setattr(Test, 'test_'+str(int(i[0])), demo(i))


if __name__ == "__main__":
    apitest = tool.APiTool()
    xlsFile = r"E:\xin\myapi_test2\apicase.xls"  # 文件路径
    sheetlist1 = apitest.xlsee(xlsFile)
    testall(sheetlist1)
    suit = unittest.makeSuite(Test)
    now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime(time.time()))
    filename = "E:\\xin\\myapi_test2\\report\\"+now+'result.html' #定义个报告存放路径，支持相对路径。
    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='自动化测试报告', description='智慧楼宇V1.0')
    runner.run(suit)
    # unittest.main()