# coding=utf-8
import unittest
import time
from new.cszdh.common import HTMLTestRunner_api
import os

import logging

t = lambda: time.time()
# logging config, the more logging config information, you can learn from "https://www.cnblogs.com/yyds/p/6901864.html"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

# this not config filename='my.log'.
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

curpath = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
report_path = os.path.join(curpath, "report")  # HTML报告存储路径


# log_path = os.path.join(now_path , "../log") # LOG日志存储路径

if not os.path.exists(report_path): os.mkdir(report_path)
case_path = os.path.join(curpath, "case")  # 测试用例路径

def add_case(casepath=case_path, rule="test*.py"):
    '''加载所有的测试用例'''
    # 定义discover方法的参数
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule,)

    return discover

def run_case(all_case, reportpath=report_path):
    '''执行所有的用例, 并把结果写入测试报告'''
    htmlreport = reportpath+r"\result.html"
    print("测试报告生成地址：%s"% htmlreport)
    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner_api.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title="测试报告",
                                               description="用例执行情况")
    # LOG日志记录
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S',
    #                     filename=log_path + '/' + now + r"result.log",
    #                     filemode='w')
    # logger = logging.getLogger()
    # logger.info(test_case)

    # 调用add_case函数返回值
    runner.run(all_case)
    fp.close()

if __name__ == "__main__":
    cases = add_case()
    run_case(cases)

