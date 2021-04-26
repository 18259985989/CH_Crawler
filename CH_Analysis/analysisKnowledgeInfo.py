# -*- coding: utf-8 -*-
# @Time : 2021/4/25 10:40
# @Author :  Meow_J

"""
知识产权
"""
from fake_useragent import UserAgent

from CH_Analysis.getDataFromJson import getcopyright
from CH_Analysis.getDataFromJson import getpatent
from CH_Analysis.getDataFromJson import geticpinfo
from CH_Analysis.getDataFromJson import getmark
from CH_Analysis.getDataFromJson import getworkright
from CH_Request.util.reqAiqicha import reqContent

class knowledgeInfoAnalysis(object):

    def __init__(self,knowledgeJson,pid,cid,batchId):
        self.Json = knowledgeJson
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
            "Referer": "https://aiqicha.baidu.com/company_detail_{}?tab=certRecord".format(self.pid),
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
            "copyright":getcopyright,#软件著作权
            "icpinfo":geticpinfo,#网站信息
            "mark":getmark,#商标信息
            "patent":getpatent,#专利信息
            "workright":getworkright,#作品著作权
        }
        urlDict = {
            "copyright": "https://aiqicha.baidu.com/detail/copyrightAjax",
            "icpinfo": "https://aiqicha.baidu.com/detail/icpinfoAjax",
            "mark": "https://aiqicha.baidu.com/c/markAjax",
            "patent": "https://aiqicha.baidu.com/detail/patentAjax",
            "workright": "https://aiqicha.baidu.com/c/workrightAjax",
        }
        for i in funcDict.keys():
            func = funcDict.get(i)
            if func is None:
                continue
            else:
                url = urlDict.get(i)
                self.getAllContent(key=i,url=url,func=func)

