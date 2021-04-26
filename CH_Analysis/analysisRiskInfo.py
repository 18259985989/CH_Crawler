# -*- coding: utf-8 -*-
# @Time : 2021/4/21 17:14
# @Author :  Meow_J

"""
重点关注
"""

from fake_useragent import UserAgent
from CH_Analysis.getDataFromJson import getlawWenshu, getdiscredit, getabnormal, getrestrictedConsumer, \
    getchattelmortgage, getuntax, gettaxviolation, getstockFreeze, getenvpunishment, getterminationcase
from CH_Analysis.getDataFromJson import getequitypledge
from CH_Analysis.getDataFromJson import getpenalties
from CH_Analysis.getDataFromJson import getopennotice
from CH_Analysis.getDataFromJson import getjudicialauction
from CH_Analysis.getDataFromJson import getCourtNoticeData
from CH_Analysis.getDataFromJson import getfilinginfo
from CH_Analysis.getDataFromJson import getillegal
from CH_Request.util.reqAiqicha import reqContent

class riskInfoAnalysis(object):
    """
    风险数据分析
    :param riskJson:
    :return:
    """

    def __init__(self,riskJson,pid,cid,batchId):
        self.Json = riskJson
        self.ua = UserAgent()
        self.pid = pid
        self.batchId = batchId
        self.cid = cid
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
            "getCourtNoticeData":getCourtNoticeData, #法院公告
            # "judicialauction":getjudicialauction, #司法拍卖
            "opennotice":getopennotice, #开庭公告
            "lawWenshu":getlawWenshu, #裁判文书
            "penalties":getpenalties, #行政处罚
            "discredit":getdiscredit, #失信被执行人
            "chattelmortgage":getchattelmortgage, #动产抵押
            "abnormal":getabnormal, #经营异常
            "filinginfo":getfilinginfo, #立案信息
            "equitypledge":getequitypledge, #股权出质
            "illegal":getillegal, #严重违法
            "restrictedConsumer":getrestrictedConsumer, #限制高消费
            "untax":getuntax, #税务非正常
            "taxviolation":gettaxviolation, #税务违法
            "stockFreeze":getstockFreeze, #股权冻结
            "envpunishment":getenvpunishment, #环境处罚
            "terminationcase":getterminationcase, #终本案件
            "executedPerson":getterminationcase, #被执行人
        }
        urlDict = {
            "getCourtNoticeData":"https://aiqicha.baidu.com/c/courtnoticeajax",
            "judicialauction":"",
            "opennotice":"https://aiqicha.baidu.com/c/opennoticeajax",
            "lawWenshu":"https://aiqicha.baidu.com/detail/lawWenshuAjax",
            "penalties":"https://aiqicha.baidu.com/detail/penaltiesAjax",
            "discredit":"https://aiqicha.baidu.com/discredit/dishonestlistAjax",
            "chattelmortgage":"",
            "abnormal":"",
            "KnowledgePledge":"",
            "filinginfo":"https://aiqicha.baidu.com/c/filinginfoAjax",
            "equitypledge":"https://aiqicha.baidu.com/c/equitypledgeAjax",
            "illegal":"",
            "restrictedConsumer":"https://aiqicha.baidu.com/detail/restrictedConsumerAjax",
            "envpunishment":"https://aiqicha.baidu.com/c/envpunishmentAjax",
        }
        for i in funcDict.keys():
            func = funcDict.get(i)
            if func is None:
                continue
            else:
                url = urlDict.get(i)
                self.getAllContent(key=i,url=url,func=func)