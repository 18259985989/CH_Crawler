# -*- coding: utf-8 -*-
# @Time : 2021/4/25 13:35
# @Author :  Meow_J

"""
经营状况
"""

from fake_useragent import UserAgent
from CH_Request.util.reqAiqicha import reqContent
from CH_Analysis.getDataFromJson import getlicense, getimportexport, getquality, getdoublecheckup, gettenderbidding, \
    getfoodquality, getrandominspection


class managerInfoAnalysis(object):

    def __init__(self,managerJson,pid,cid,batchId):
        self.Json = managerJson
        self.ua = UserAgent()
        self.pid = pid
        self.cid = cid
        self.batchId = batchId
        self.flag = "Fail"
        self.headers = {
            "Host": "aiqicha.baidu.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.ua.random,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://aiqicha.baidu.com/company_detail_{}?tab=operatingCondition".format(self.pid),
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
                func(dataList=dataList,cid=self.cid,batchId=self.batchId)
            elif total > 10 and total <= 100:
                resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                if resp != self.flag:
                    data = resp.get("data")
                    dataList = data.get("list")
                    func(dataList=dataList,cid=self.cid,batchId=self.batchId)
            else:
                page = int(total / 100) + 1
                for i in range(1, page+1):
                    self.payload.update({"p": i})
                    resp = reqContent(url=url, headers=self.headers, payload=self.payload).reqJson()
                    if resp != self.flag:
                        data = resp.get("data")
                        dataList = data.get("list")
                        func(dataList=dataList,cid=self.cid,batchId=self.batchId)
                self.payload.update({"p": 1})

    def run(self):
        funcDict = {
            "license":getlicense,#行政许可
            "importexport":getimportexport,#进出口信用
            "quality":getquality,#质量监督检查
            "doublecheckup":getdoublecheckup,#双随机检查
            "randominspection":getrandominspection,#抽查检查
            "tenderbidding":gettenderbidding,#招投标
            "foodquality":getfoodquality,#食品抽查检查
        }
        urlDict = {
            "license":"https://aiqicha.baidu.com/detail/licenseAjax",
            "importexport":"",
            "quality":"https://aiqicha.baidu.com/detail/qualityAjax",
            "doublecheckup":"",
            "tenderbidding":"https://aiqicha.baidu.com/c/tenderbiddingAjax",
            "foodquality":"https://aiqicha.baidu.com/detail/foodqualityAjax",
        }
        for i in funcDict.keys():
            func = funcDict.get(i)
            if func is None:
                continue
            else:
                url = urlDict.get(i)
                self.getAllContent(key=i, url=url, func=func)

