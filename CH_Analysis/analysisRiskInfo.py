# -*- coding: utf-8 -*-
# @Time : 2021/4/21 17:14
# @Author :  Meow_J

"""
爱企查中风险数据清洗并入库
"""


import pymysql
from fake_useragent import UserAgent
from CH_Request.util.reqAiqicha import reqContent

class riskInfoAnalysis(object):
    """
    风险数据分析并入库
    :param riskJson:
    :return:
    """

    def __init__(self,riskJson,pid):
        self.Json = riskJson
        self.ua = UserAgent()
        self.pid = pid
        self.headers = {
            "Host":"aiqicha.baidu.com",
            "Connection":"keep-alive",
            "Accept":"application/json, text/plain, */*",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":self.ua.random,
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
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

    def lawWenshu(self):
        data = self.Json.get("lawWenshu")
        total = data.get("total")
        if total != 0 and total != "":
            if total < 10:
                #总条数小于10直接获取  （详情内容需要根据Url再去请求获取）
                dataList = data.get("list")
                for i in dataList:
                    type = i.get("type") #案由
                    verdictDate = i.get("verdictDate") #日期
                    caseNo = i.get("caseNo") #案号
                    role = i.get("role") #角色
                    wenshuName = i.get("wenshuName") #文书名称
                    wenshuId = i.get("wenshuId") #文书ID
                    detailUrl = i.get("detailUrl") #文书详情URL

            else:
                #总条数大于10条存在分页
                url = "https://aiqicha.baidu.com/detail/lawWenshuAjax"
                self.headers.update({"Referer":'https://aiqicha.baidu.com/company_detail_{}?tab=risk'.format(self.pid)})
                payload = {
                    "p":2,  #暂时写2 后面update
                    "size":100,
                    "pid":self.pid,
                }
                reqContent(url=url,headers=self.headers,payload=payload).reqJson()






    def run(self):
        self.KnowledgePledge()
        print(2)









