# -*- coding: utf-8 -*-
# @Time : 2021/4/25 11:44
# @Author :  Meow_J


"""
企业发展
"""

from fake_useragent import UserAgent
from CH_Request.util.reqAiqicha import reqContent
from CH_Analysis.getDataFromJson import getbrandProject
from CH_Analysis.getDataFromJson import getinvestorlist
from CH_Analysis.getDataFromJson import getprojectSimilarsInfo
from CH_Analysis.getDataFromJson import getCompPersonList
from CH_Analysis.getDataFromJson import projectFinance


class developInfoAnalysis(object):

    def __init__(self,developJson,pid):
        self.Json = developJson
        self.ua = UserAgent()
        self.pid = pid
        self.flag = "Fail"
        self.headers = {
            "Host": "aiqicha.baidu.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.ua.random,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://aiqicha.baidu.com/company_detail_{}?tab=companyDevelop".format(self.pid),
        }
        self.payload = {
            "p": 1,
            "size": 100,  # 可以写大  减小请求次数
            "pid": self.pid,
        }
        self.run()

    def getAllContent(self,key,url,func):
        """
        通用获取所有类型数据方法
        :param url:
        :return:
        """
        data = self.Json.get(key)
        total = data.get("total")
        if total != 0 and total != "":
            if total <= 10:
                # 总条数小于10直接获取  （详情内容需要根据Url再去请求获取）
                dataList = data.get("list")
                func(dataList=dataList)
            elif total > 10 and total <= 100:
                resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                if resp != self.flag:
                    data = resp.get("data")
                    dataList = data.get("list")
                    func(dataList=dataList)
            else:
                page = int(total / 100) + 1
                for i in range(1, page+1):
                    self.payload.update({"p": i})
                    resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                    if resp != self.flag:
                        data = resp.get("data")
                        dataList = data.get("list")
                        func(dataList=dataList)
                self.payload.update({"p": 1})

    def run(self):
        funcDict = {
            "brandProject":getbrandProject, #企业品牌项目
            "getCompPersonList":getCompPersonList,
            "investorlist":getinvestorlist,
            "projectFinance":projectFinance,
            "projectSimilarsInfo":getprojectSimilarsInfo,
        }
        urlDict = {
            "brandProject":"",
            "getCompPersonList":"https://aiqicha.baidu.com/m/getCompPersonListAjax",
            "investorlist":"",
            "projectFinance":"",
            "projectSimilarsInfo":"https://aiqicha.baidu.com/project/projectSimilarsInfoAjax",
        }
        for i in funcDict.keys():
            func = funcDict.get(i)
            if func is None:
                continue
            else:
                url = urlDict.get(i)
                self.getAllContent(key=i,url=url,func=func)