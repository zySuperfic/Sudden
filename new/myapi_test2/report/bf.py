#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-12-03 10:07
import xlrd
import requests
class APiTool:
    # 调取表格中用例方法
    def xlsee(self, xlsFile):
        sheetlist = []  # 用来保存表格所有数据
        rqapi = xlrd.open_workbook(xlsFile)   # 获得文件对象
        sheet_name = rqapi.sheet_names()[0]  # 获取第一个sheet名称
        sheet = rqapi.sheet_by_name(sheet_name)  # 获取第一个sheet对象
        nrow = sheet.nrows   # 获取行总数
        for i in range(1,nrow):
            sheetlist.append(sheet.row_values(i))
        return sheetlist

    # 请求方法
    def request(self, rqtype, rqurl, paramete, headers):
        if rqtype == "get":
            apiresult = requests.get(url=rqurl, params=paramete, headers=headers)  # 发送请求
            return apiresult
        if rqtype == "post":
            apiresult = requests.post(url=rqurl, data=paramete, headers=headers)
            return apiresult
        else:
            print("请求参数错误，请求类型只支持get+post，请求地址支持string，参数支持dict")

    # 对返回的json值进行深度断言

    # def compare_json_data(self,A, B, L = [], xpath = '.'):
    #     if isinstance(A, list) and isinstance(B, list):
    #         for i in range(len(A)):
    #             try:
    #                 self.compare_json_data(A[i], B[i], L, xpath + '[%s]' % str(i))
    #             except:
    #                 L.append('▇▇▇ A中的key %s[%s]未在B中找到\n' % (xpath, i))
    #     if isinstance(A, dict) and isinstance(B, dict):
    #         for i in A:
    #             try:
    #                 B[i]
    #             except:
    #                 L.append('▇▇▇ A中的key %s/%s 未在B中找到\n' % (xpath, i))
    #                 continue
    #             if not (isinstance(A.get(i), (list, dict)) or isinstance(B.get(i), (list, dict))):
    #                 if type(A.get(i)) != type(B.get(i)):
    #                     L.append('▇▇▇ 类型不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s \n' % (xpath, i, type(A.get(i)), type(B.get(i))))
    #                 elif A.get(i) != B.get(i):
    #                     L.append('▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s/%s  ►►► A is %s, B is %s \n' % (xpath, i, A.get(i), B.get(i)))
    #                 continue
    #             self.compare_json_data(A.get(i), B.get(i), L, xpath + '/' + str(i))
    #         return
    #     if type(A) != type(B):
    #         L.append('▇▇▇ 类型不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s \n' % (xpath, type(A), type(B)))
    #     elif A != B and type(A) is not list:
    #         L.append('▇▇▇ 仅内容不同参数在[A]中的绝对路径:  %s  ►►► A is %s, B is %s \n' % (xpath, A, B))
    #     return L
    #
    # def Assert(self,A,B):
    #     C = []
    #     self.compare_json_data(A, B, C)
    #     assert len(C) == 0, "\n"+"".join(C)

if __name__ == "__main__":
        apitest = APiTool()
        # # xlsFile = r"D:\myapi_test\apicase.xls"  # 文件路径
        # # sheetlist1 = apitest.xlsee(xlsFile)
        # # print(type(sheetlist1[0][0]))
        # a= {'b':[1,2,5,8],'c':3,'d':2,'f':[1,2,3],'g':[1,2,3,[2,'2',2]],'h':'5'}
        # b= {'b':[1,2,'3'],'c':2,'e':'4','f':[1,2,3,5],'g':[1,2,3,[1,2]],'h':[1,2]}
        # apitest.Assert(a,b)