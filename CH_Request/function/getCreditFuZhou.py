# 信用福州
import base64
import json
import threading
from urllib.parse import quote
from CH_Request.util.reqContent import postContent

class CreditFuZhou(threading.Thread):

    def __init__(self,comName):
        threading.Thread.__init__(self)
        print("启动信用福州爬取程序")
        self.comName = comName


    def getComId(self):
        """
        获取公司Id
        :return:
        """

        url = 'http://credit.fuzhou.gov.cn/xyfz/api/service/queryQyxydaPage'
        headers = {
            "Host":"credit.fuzhou.gov.cn",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Content-Length":"151",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Accept-Encoding":"gzip, deflate",
            "Origin":"http://credit.fuzhou.gov.cn",
            "Referer":"http://credit.fuzhou.gov.cn/qyxy/qyxyfw/?tab=0&name={}".format(quote(self.comName)),
            "Accept":"application/json, text/javascript, */*; q=0.01",
        }
        Form ={
            "pageSize":"50",
            "currentPage":"1",
            "qymc":"{}".format(self.comName),
        }
        # 获取base64加密前的数据 内容为json
        resp = postContent(url=url,headers=headers,payload=Form)
        beforeDecode = resp.get("data")
        afterDecode = json.loads(str(base64.b64decode(beforeDecode),encoding="utf-8"))
        total = afterDecode.get("toatl")
        if total != 0:
            dataList = afterDecode.get("dataList")
            for i in dataList:
                if i.get("qymc") != self.comName:
                    print("获取到的公司名称与输入不符，获取为{}".format(i.get("qymc")))
                else:
                    comId = i.get("id")
                    return comId
        else:
            print("获取到公司Id数量为空")

    def reqBaseInfo(self):
        comId = self.getComId()
        url = 'http://credit.fuzhou.gov.cn/xyfz/api/service/selectQyxydaById'
        headers = {
            "Host": "credit.fuzhou.gov.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Content-Length": "27",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Origin": "http://credit.fuzhou.gov.cn",
            "Referer": "http://credit.fuzhou.gov.cn/qyxy/qyxyfw/detail.htm?id={}".format(comId),
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        Form = {
            "id":comId
        }
        resp = postContent(url=url,headers=headers,payload=Form)
        beforeDecode = resp.get("data")
        afterDecode = json.loads(str(base64.b64decode(beforeDecode), encoding="utf-8"))
        data = afterDecode.get("data")
        self.getBaseInfo(data=data)


    def getBaseInfo(self,data):
        """
        抽取出基本信息
        :return:
        """
        BaseInfo = data.get("qydatgxx")
        qylx = BaseInfo.get("qylx") #企业类型
        zcdz = BaseInfo.get("zcdz") #注册地址
        zczb = BaseInfo.get("zczb") #注册资本
        jyjsrq = BaseInfo.get("jyjsrq") #经营期限至
        jyksrq = BaseInfo.get("jyksrq") #经营期限自
        tyshxydm = BaseInfo.get("tyshxydm") #统一社会信用代码
        gszch = BaseInfo.get("gszch") #注册号
        jyfw = BaseInfo.get("jyfw") #经营范围
        fddbr = BaseInfo.get("fddbr") #法人代表
        Data = (self.comName,qylx,zcdz,zczb,jyjsrq,jyksrq,tyshxydm,gszch,jyfw,fddbr)
        print(Data)
        print("信用福州程序结束")

    def run(self):
        self.reqBaseInfo()