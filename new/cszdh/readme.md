# ����

���ߣ��Ϻ�-����
����QQȺ��588402570

# ǰ��
1.����׼����
- python3.6
- requests
- xlrd
- openpyxl
- HTMLTestRunner_api

2.Ŀǰʵ�ֵĹ��ܣ�
- ��װrequests���󷽷�
- ��excel��д�ӿ��������
- ���������������һ��excel���棬���д��excel
- ��unittest+ddt��������ģʽִ��
- HTMLTestRunner���ɿ��ӻ���html����
- ����û�й����ĵ����ӿ������ǿ�������ִ�еģ���Ҫ��¼�Ļ�д��setUpclass���session�ﱣ��cookies
- token�����Ĳ���ʵ��
- logging��־�ļ���ʱδ����

3.Ŀǰ��֪��ȱ�ݣ�
- �޷�ʵ�ֲ����������ϸ�����Ľ�����¸�����Ĳ�������token
- �ӿ�������������ظ��ģ�Ŀǰδ������key1=value1&key1=value2,����key��һ����������Ҫ��Ԫ��洢��Ŀǰ��ʱδ�ж�
- ���ɵ�excel��ʽδ�������������Ż���ʽ
- python���ֿ�������ģ�鵼�뱨������

# ��Ŀ�ṹ

![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323111753095-1203930062.png)




# excel��������

![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323102605467-2039444472.png)



# xlrd��excel����

1.�ȴ�excel�����ȡ�������ݣ������ֵ��ʽ

![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323102436666-427613061.png)


```
# coding:utf-8

# ���ߣ��Ϻ�-����
# QQȺ��226296743

import xlrd
class ExcelUtil():
    def __init__(self, excelPath, sheetName="Sheet1"):
        self.data = xlrd.open_workbook(excelPath)
        self.table = self.data.sheet_by_name(sheetName)
        # ��ȡ��һ����Ϊkeyֵ
        self.keys = self.table.row_values(0)
        # ��ȡ������
        self.rowNum = self.table.nrows
        # ��ȡ������
        self.colNum = self.table.ncols

    def dict_data(self):
        if self.rowNum <= 1:
            print("������С��1")
        else:
            r = []
            j = 1
            for i in list(range(self.rowNum-1)):
                s = {}
                # �ӵڶ���ȡ��Ӧvaluesֵ
                s['rowNum'] = i+2
                values = self.table.row_values(j)
                for x in list(range(self.colNum)):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

if __name__ == "__main__":
    filepath = "debug_api.xlsx"
    sheetName = "Sheet1"
    data = ExcelUtil(filepath, sheetName)
    print(data.dict_data())
```
# openpyxlд������


1.�ٷ�װһ��д��excel���ݵķ���

```
# coding:utf-8
from openpyxl import load_workbook
import openpyxl

# ���ߣ��Ϻ�-����
# QQȺ��226296743

def copy_excel(excelpath1, excelpath2):
    '''����excek����excelpath1���ݸ��Ƶ�excelpath2'''
    wb2 = openpyxl.Workbook()
    wb2.save(excelpath2)
    # ��ȡ����
    wb1 = openpyxl.load_workbook(excelpath1)
    wb2 = openpyxl.load_workbook(excelpath2)
    sheets1 = wb1.sheetnames
    sheets2 = wb2.sheetnames
    sheet1 = wb1[sheets1[0]]
    sheet2 = wb2[sheets2[0]]
    max_row = sheet1.max_row         # �������
    max_column = sheet1.max_column   # �������

    for m in list(range(1,max_row+1)):
        for n in list(range(97,97+max_column)):   # chr(97)='a'
            n = chr(n)                            # ASCII�ַ�
            i ='%s%d'% (n, m)                     # ��Ԫ����
            cell1 = sheet1[i].value               # ��ȡdata��Ԫ������
            sheet2[i].value = cell1               # ��ֵ��test��Ԫ��

    wb2.save(excelpath2)                 # ��������
    wb1.close()                          # �ر�excel
    wb2.close()

class Write_excel(object):
    '''�޸�excel����'''
    def __init__(self, filename):
        self.filename = filename
        self.wb = load_workbook(self.filename)
        self.ws = self.wb.active  # ����sheet

    def write(self, row_n, col_n, value):
        '''д�����ݣ���(2,3��"hello"),�ڶ��е�����д������"hello"'''
        self.ws.cell(row_n, col_n).value = value
        self.wb.save(self.filename)

if __name__ == "__main__":
    copy_excel("debug_api.xlsx", "testreport.xlsx")
    wt = Write_excel("testreport.xlsx")
    wt.write(4, 5, "HELLEOP")
    wt.write(4, 6, "HELLEOP")

```

# ��װrequest���󷽷�

1.�Ѵ�excel�������������Ϊ�����������װrequests���󷽷���������������������ؽ��

2.Ϊ�˲���Ⱦ���Ե����ݣ��������ʱ���Ƚ����Ե�excel���ƶ�Ӧ���µ�excel

3.�Ѳ��Է��صĽ�������µ�excel����д������
```
# coding:utf-8
import json
import requests
from excelddtdriver.common.readexcel import ExcelUtil
from excelddtdriver.common.writeexcel import copy_excel, Write_excel

# ���ߣ��Ϻ�-����
# QQȺ��226296743


def send_requests(s, testdata):
    '''��װrequests����'''
    method = testdata["method"]
    url = testdata["url"]
    # url�����params����
    try:
        params = eval(testdata["params"])
    except:
        params = None
    # ����ͷ��headers
    try:
        headers = eval(testdata["headers"])
        print("����ͷ����%s" % headers)
    except:
        headers = None
    # post����body����
    type = testdata["type"]

    test_nub = testdata['id']
    print("*******����ִ��������-----  %s  ----**********" % test_nub)
    print("����ʽ��%s, ����url:%s" % (method, url))
    print("����params��%s" % params)

    # post����body����
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}

    # �жϴ�data���ݻ���json
    if type == "data":
        body = bodydata
    elif type == "json":
        body = json.dumps(bodydata)
    else:
        body = bodydata
    if method == "post": print("post����body����Ϊ��%s ,body����Ϊ��%s" % (type, body))

    verify = False
    res = {}   # ���ܷ�������

    try:
        r = s.request(method=method,
                      url=url,
                      params=params,
                      headers=headers,
                      data=body,
                      verify=verify
                       )
        print("ҳ�淵����Ϣ��%s" % r.content.decode("utf-8"))
        res['id'] = testdata['id']
        res['rowNum'] = testdata['rowNum']
        res["statuscode"] = str(r.status_code)  # ״̬��ת��str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())   # �ӿ�����ʱ��תstr
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        res["msg"] = ""
        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print("�������Խ��:   %s---->%s" % (test_nub, res["result"]))
        else:
            res["result"] = "fail"
        return res
    except Exception as msg:
        res["msg"] = str(msg)
        return res

def wirte_result(result, filename="result.xlsx"):
    # ���ؽ��������row_nub
    row_nub = result['rowNum']
    # д��statuscode
    wt = Write_excel(filename)
    wt.write(row_nub, 8, result['statuscode'])       # д�뷵��״̬��statuscode,��8��
    wt.write(row_nub, 9, result['times'])            # ��ʱ
    wt.write(row_nub, 10, result['error'])            # ״̬���200ʱ�ķ�����Ϣ
    wt.write(row_nub, 12, result['result'])           # ���Խ�� pass ����fail
    wt.write(row_nub, 13, result['msg'])           # ���쳣

if __name__ == "__main__":
    data = ExcelUtil("debug_api.xlsx").dict_data()
    print(data[0])
    s = requests.session()
    res = send_requests(s, data[0])
    copy_excel("debug_api.xlsx", "result.xlsx")
    wirte_result(res, filename="result.xlsx")
```

# ��������unittest+ddt

1.����������unittest����齨������ddt��������ģʽ������ִ������

```
# coding:utf-8
import unittest
import ddt
import os
import requests
from excelddtdriver.common import base_api
from excelddtdriver.common import readexcel
from excelddtdriver.common import writeexcel

# ���ߣ��Ϻ�-����
# QQȺ��226296743

# ��ȡdemo_api.xlsx·��
curpath = os.path.dirname(os.path.realpath(__file__))
testxlsx = os.path.join(curpath, "demo_api.xlsx")

# ����demo_api.xlsx�ļ���report��
report_path = os.path.join(os.path.dirname(curpath), "report")
reportxlsx = os.path.join(report_path, "result.xlsx")

testdata = readexcel.ExcelUtil(testxlsx).dict_data()
@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = requests.session()
        # ����е�¼�Ļ������������ȵ�¼��
        writeexcel.copy_excel(testxlsx, reportxlsx) # ����xlsx

    @ddt.data(*testdata)
    def test_api(self, data):
        # �ȸ���excel���ݵ�report
        res = base_api.send_requests(self.s, data)

        base_api.wirte_result(res, filename=reportxlsx)
        # ���� checkpoint
        check = data["checkpoint"]
        print("����->��%s"%check)
        # ���ؽ��
        res_text = res["text"]
        print("����ʵ�ʽ��->��%s"%res_text)
        # ����
        self.assertTrue(check in res_text)

if __name__ == "__main__":
    unittest.main()
```

# ���ɱ���

1.��HTMLTestRunner����html���棬��������������ƣ��ĳ���HTMLTestRunner_api.py
���ļ���selenium�ı�����ͨ�õģ�github������[https://github.com/yoyoketang/selenium_report/tree/master/selenium_report](https://github.com/yoyoketang/selenium_report/tree/master/selenium_report)

```
# coding=utf-8
import unittest
import time
from excelddtdriver.common import HTMLTestRunner_api
import os

# ���ߣ��Ϻ�-����
# QQȺ��226296743

curpath = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(curpath, "report")
if not os.path.exists(report_path): os.mkdir(report_path)
case_path = os.path.join(curpath, "case")

def add_case(casepath=case_path, rule="test*.py"):
    '''�������еĲ�������'''
    # ����discover�����Ĳ���
    discover = unittest.defaultTestLoader.discover(casepath,
                                                  pattern=rule,)

    return discover

def run_case(all_case, reportpath=report_path):
    '''ִ�����е�����, ���ѽ��д����Ա���'''
    htmlreport = reportpath+r"\result.html"
    print("���Ա������ɵ�ַ��%s"% htmlreport)
    fp = open(htmlreport, "wb")
    runner = HTMLTestRunner_api.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title="���Ա���",
                                               description="����ִ�����")

    # ����add_case��������ֵ
    runner.run(all_case)
    fp.close()

if __name__ == "__main__":
    cases = add_case()
    run_case(cases)

```

2.���ɵ�excel����

![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323102540571-718340736.png)


3.���ɵ�html����

![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323102617264-2071969634.png)



---------------------------------python�ӿ��Զ����ѳ���-------------------------
���˴����С��������������һƪ���ص�Դ��

ȫ�鹺���ַ [https://yuedu.baidu.com/ebook/585ab168302b3169a45177232f60ddccda38e695](https://yuedu.baidu.com/ebook/585ab168302b3169a45177232f60ddccda38e695)
![](https://images2018.cnblogs.com/blog/1070438/201803/1070438-20180323104725561-146885286.png)