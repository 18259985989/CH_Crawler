# -*- coding: utf-8 -*-
# @Time : 2021/4/15 21:15
# @Author :  Meow_J

"""
爱企查爬虫
"""

import re
import os
import json
import requests
import sys
from fake_useragent import UserAgent

dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir_path)

from CH_Analysis.analysisBaseInfo import getBaseData
from CH_Analysis.analysisBaseInfo import Shareholders
from CH_Analysis.analysisBaseInfo import Directors
from CH_Analysis.analysisBaseInfo import ChangeRecord
from CH_Analysis.analysisBaseInfo import Invest
from CH_Analysis.analysisBaseInfo import Hold
from CH_Analysis.analysisBaseInfo import Branch
from CH_Analysis.analysisRiskInfo import riskInfoAnalysis
from CH_Request.util.proxyPool import proxyPool as Proxy
from CH_Request.util.reqAiqicha import reqContent


class getAiqicha(object):

    def __init__(self,comName):
        self.proxy = Proxy()
        self.ua = UserAgent()
        self.comName = comName
        self.errCount = 0
        self.newTabs = []
        self.flag = "Fail"


    def reqCompanyId(self):
        url = 'https://aiqicha.baidu.com/s'
        headers = {
            "Host":"aiqicha.baidu.com",
            "Connection":"keep-alive",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":self.ua.random,
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer":"https://aiqicha.baidu.com/",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }
        payload = {
            "q":self.comName,
            "t":0
        }
        while True:
            if self.errCount <5:
                try:
                    Ip = self.proxy.reqProxy()
                    resp = requests.get(url=url,headers=headers,params=payload,proxies={"https":Ip},timeout=10)
                except Exception as e:
                    self.errCount += 1
                    print("请求公司Id时出现异常：{}".format(e))
                else:
                    if resp.status_code != 200:
                        self.errCount += 1
                        print("请求公司Id时状态码不为200.")
                    else:
                        resList = re.findall(r'"result":(.*?)};',resp.text,re.S)
                        if len(resList)!= 0:
                            res = json.loads(resList[0])
                            resultList = res.get("resultList")
                            totalNumFound = res.get("totalNumFound")
                            if totalNumFound != 0:
                                for i in resultList:
                                    entName = i.get("titleName")
                                    if entName == self.comName:
                                        pid = i.get("pid")
                                        print(pid)
                                        return pid
                                    else:
                                        continue
                                print("查找到的公司与输入公司名不符")
                                return self.flag
                            else:
                                print("查找到总数为0，请重新输入公司名")
                                return self.flag
                        else:
                            print("获取到的文本内容有误")
                            self.errCount +=1
            else:
                print("重试次数超过上限。停止访问")
                return self.flag

    def reqBaseInfo(self,pid):
        """
        公司基本信息(涵盖工商信息及其他基本信息)
        :return:
        """
        url = "https://aiqicha.baidu.com/detail/basicAllDataAjax"
        allDataList = []
        baesFunDict = {
            "shareholders":Shareholders,
            "directors":Directors,
            "branch":Branch,
            "change":ChangeRecord,
            "invest":Invest,
            "hold":Hold,
        }
        headers = {
            "Host":"aiqicha.baidu.com",
            "Connection":"keep-alive",
            "Accept":"application/json, text/plain, */*",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":self.ua.random,
            "Referer":"https://aiqicha.baidu.com/company_detail_{}".format(pid),
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
        }
        payload = {
            "pid":pid,
        }

        resJson = reqContent(url=url,headers=headers,payload=payload).reqJson()
        if resJson != self.flag:
            self.newTabs =  resJson.get("data").get("basicData").get("newTabs") #该公司所拥有的数据列表
            getBaseData(Json=resJson) #不论如何先插入基本数据信息

            for i in self.newTabs:
                tab = i.get("id")
                total = i.get("total")
                if tab == "basic":
                    if total == 0 or total == "":
                        print("无其他基本信息")
                        break
                    childList = i.get("children")
                    for k in childList:
                        childTotal = k.get("total")
                        if childTotal == 0 or childTotal == "":
                            continue
                        allDataList.append(k.get("id"))
                else:
                    continue
            for fun in allDataList:
                if fun in baesFunDict.keys():
                    baesFunDict.get(fun)(Json=resJson)
            return None
        else:
            print("获取到resJson为空或有异常")


    def reqRiskInfo(self,pid):
        """
        公司重点关注信息（风险信息）
        :param pid:
        :return:
        """
        url = "https://aiqicha.baidu.com/detail/focalPointAjax"
        headers = {
            "Host": "aiqicha.baidu.com",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.ua.random,
            "Referer": "https://aiqicha.baidu.com/company_detail_{}?tab=risk".format(pid),
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
        payload = {
            "pid": pid,
        }

        riskJson = reqContent(url=url, headers=headers, payload=payload).reqJson()
        if riskJson != self.flag:
            data = riskJson.get("data")
            riskInfoAnalysis(riskJson=data,pid=pid)

    def reqKnowledgeInfo(self,pid):
        """
        知识产权信息
        :param pid:
        :return:
        """
        pass

    def reqComDevelopInfo(self,pid):
        """
        企业发展信息
        :param pid:
        :return:
        """
        pass

    def reqManagerInfo(self,pid):
        """
        经营状况信息
        :param pid:
        :return:
        """
        pass



    def run(self):
        pid = self.reqCompanyId()
        self.reqBaseInfo(pid=pid)  #基本信息及其他基础信息
        funDict = {
            "risk":self.reqRiskInfo,
            "certRecord":self.reqKnowledgeInfo,
            "companyDevelop":self.reqComDevelopInfo,
            "operatingCondition":self.reqManagerInfo,
        }
        for obj in self.newTabs:
            id = obj.get("id")
            total = obj.get("total")
            if id in funDict.keys():
                if total == 0 or total == "":
                    continue
                else:
                    funDict.get(id)(pid=pid)
            else:
                pass



if __name__ == '__main__':
    a = getAiqicha(comName='福建诚华信用管理有限公司')
    a.run()