# -*- coding: utf-8 -*-
# @Time : 2021/4/21 17:14
# @Author :  Meow_J

"""
爱企查中风险数据清洗
"""

from fake_useragent import UserAgent
from CH_Analysis.getDataFromJson import getlawWenshu
from CH_Analysis.getDataFromJson import getpenalties
from CH_Analysis.getDataFromJson import getopennotice
from CH_Analysis.getDataFromJson import getjudicialauction
from CH_Request.util.reqAiqicha import reqContent

class riskInfoAnalysis(object):
    """
    风险数据分析
    :param riskJson:
    :return:
    """

    def __init__(self,riskJson,pid):
        self.Json = riskJson
        self.ua = UserAgent()
        self.pid = pid
        self.flag = "Fail"
        self.headers = {
            "Host":"aiqicha.baidu.com",
            "Connection":"keep-alive",
            "Accept":"application/json, text/plain, */*",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":self.ua.random,
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Referer":"https://aiqicha.baidu.com/company_detail_{}?tab=risk".format(self.pid),
        }
        self.payload = {
            "p": 1,
            "size": 100,  # 可以写大  减小请求次数
            "pid": self.pid,
        }
        self.run()


    def KnowledgePledge(self):
        """
        知识产权出质
        :return:
        """
        data = self.Json.get("KnowledgePledge")
        total = data.get("total")
        dataList = data.get("list")
        if total != 0 and total != "":
            pass

    def abnormal(self):
        """
        经营异常
        :return:
        """
        data = self.Json.get("abnormal")
        total = data.get("total")
        dataList = data.get("list")
        if total != 0 and total != "":
            pass

    def chattelmortgage(self):
        """
        动产抵押
        :return:
        """
        data = self.Json.get("chattelmortgage")
        total = data.get("total")
        dataList = data.get("list")
        if total != 0 and total != "":
            pass

    def discredit(self):
        """
        失信被执行人
        :return:
        """
        data = self.Json.get("discredit")
        total = data.get("total")
        dataList = data.get("list")
        if total != 0 and total != "":
            pass

    def penalties(self):
        """
        行政处罚
        :return:
        """
        url = "https://aiqicha.baidu.com/detail/penaltiesAjax"
        data = self.Json.get("penalties")
        total = data.get("total")
        if total != 0 and total != "":
            if total<10:
                dataList = data.get("list")
                getpenalties(dataList=dataList)
            elif total >10 and total <100:
                resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                if resp != self.flag:
                    Message = resp.get("data")
                    MessageList = Message.get("list")
                    getpenalties(dataList=MessageList)
            else:
                page = int(total / 100) + 1
                for i in range(1,page):
                    self.payload.update({"p": i})
                    resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                    if resp != self.flag:
                        Message = resp.get("data")
                        MessageList = Message.get("list")
                        getpenalties(dataList=MessageList)
                self.payload.update({"p": 1})  # 初始化payload

    def lawWenshu(self):
        """
        裁判文书
        :return:
        """
        url = "https://aiqicha.baidu.com/detail/lawWenshuAjax"
        data = self.Json.get("lawWenshu")
        total = data.get("total")
        if total != 0 and total != "":
            if total < 10:
                #总条数小于10直接获取  （详情内容需要根据Url再去请求获取）
                dataList = data.get("list")
                getlawWenshu(dataList=dataList)
            elif total >10 and total <100:
                resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                if resp != self.flag:
                    data = resp.get("data")
                    dataList = data.get("list")
                    getlawWenshu(dataList=dataList)
            else:
                #总条数大于10条存在分页
                page = int(total/100)+1
                for i in range(1,page):
                    self.payload.update({"p":i})
                    resp = reqContent(url=url,headers=self.headers,payload=self.payload).reqJson()
                    if resp != self.flag:
                        data = resp.get("data")
                        dataList = data.get("list")
                        getlawWenshu(dataList=dataList)
                self.payload.update({"p":1})  #初始化payload

    def opennotice(self):
        """
        开庭公告
        :return:
        """
        url = "https://aiqicha.baidu.com/c/opennoticeajax"
        data = self.Json.get("opennotice")
        total = data.get("total")
        if total != 0 and total != "":
            if total < 10:
                #总条数小于10直接获取  （详情内容需要根据Url再去请求获取）
                dataList = data.get("list")
                getopennotice(dataList=dataList)
            elif total >10 and total <100:
                resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                if resp != self.flag:
                    data = resp.get("data")
                    dataList = data.get("list")
                    getopennotice(dataList=dataList)
            else:
                page = int(total/100)+1
                for i in range(1,page):
                    self.payload.update({"p":i})
                    resp = reqContent(url=url,headers=self.headers,payload=self.payload).reqJson()
                    if resp != self.flag:
                        data = resp.get("data")
                        dataList = data.get("list")
                        getopennotice(dataList=dataList)
                self.payload.update({"p":1})  #初始化payload

    def judicialauction(self):
        """
        司法拍卖
        :return:
        """
        url = ""
        data = self.Json.get("judicialauction")
        total = data.get("total")
        if total != 0 and total != "":
            if total < 10:
                # 总条数小于10直接获取  （详情内容需要根据Url再去请求获取）
                dataList = data.get("list")
                getjudicialauction(dataList=dataList)
            elif total > 10 and total < 100:
                pass
            else:
                pass

    def getCourtNoticeData(self):
        """
        法院公告
        :return:
        """
        url = "https://aiqicha.baidu.com/c/courtnoticeajax"
        data = self.Json.get("getCourtNoticeData")
        total = data.get("total")








    def run(self):
        self.KnowledgePledge()











