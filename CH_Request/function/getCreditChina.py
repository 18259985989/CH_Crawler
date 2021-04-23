# 信用中国
import threading
from CH_Request.util.reqContent import reqContent

class getCreditChina(threading.Thread):

    def __init__(self,comName):
        threading.Thread.__init__(self)
        print("启动信用中国爬取程序")
        self.comName = comName
        self.header = {
        "Host":"public.creditchina.gov.cn",
        "Connection":"Connection",
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Origin":"https://www.creditchina.gov.cn",
        "Referer":"https://www.creditchina.gov.cn",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
    }


    def getuuid(self):
        url = "https://public.creditchina.gov.cn/private-api/catalogSearchHome"
        payload = {
            "keyword": "{}".format(self.comName),
            "scenes": "defaultScenario",
            "tableName": "credit_xyzx_tyshxydm",
            "searchState": "2",
        }
        res = reqContent(url=url,headers=self.header,payload=payload)
        if res.get("message") == "成功" or res.get("status") == 1:
            dataList = res.get("data").get("list")
            for i in dataList:
                accurate_entity_name = i.get("accurate_entity_name")
                if accurate_entity_name != self.comName:
                    print("获取uuid时获取到的公司名与输入公司名不符!")
                else:
                    uuid = i.get("uuid")
                    return uuid
        else:
            print("获取uuid时出现错误")

    def getDataTypeCount(self):
        """
        获取数据类型数量
        :return:
        """
        url = "https://public.creditchina.gov.cn/private-api/searchDateTypeCount"
        payload = {
            "entityType":"1",
            "searchState":"1",
            "keyword":self.comName,
        }
        res = reqContent(url=url,headers=self.header,payload=payload)
        if res.get("message") == "成功" or res.get("status") == 1:
            dataDict = res.get("data")
            for key in dataDict.keys():
                nums = dataDict.get(key)
                if nums != 0:
                    print("{}:{}的数量为{}".format(self.comName,key,nums))
                    self.getDataSource(type=key)
                else:
                    print("{}:{}的数量为0".format(self.comName,key))
        else:
            print("获取类别数量时出现错误")


    def getDataSource(self,type):
        url = "https://public.creditchina.gov.cn/private-api/typeSourceSearch"
        payload = {
            "type":type,
            "keyword":self.comName,
            "searchState":"1",
            "entityType":"1",
            "scenes":"defaultscenario",
            "page":"1",
            "pageSize":"100",
        }
        res = reqContent(url=url,headers=self.header,payload=payload)
        if res.get("message") == "成功" or res.get("status") == 1:
            dataList = res.get("data").get("list")
            # print(dataList)
            for i in dataList:
                columnList = i.get('columnList')
                for k in columnList:

                    print(i.get("entity").get(k))
                print("="*50)
        else:
            print("获取{}中{}时发生异常".format(self.comName,type))
        print("信用中国程序结束")


    def run(self):
        self.getDataTypeCount()