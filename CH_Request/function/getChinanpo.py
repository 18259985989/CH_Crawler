# 全国社会组织信用信息公开平台

import json
import base64
import pymysql
from CH_Request.util.reqContent import postContent


class getChinanpo(object):

    def __init__(self,orgName):
        self.orgName = orgName

    def getOrgId(self):
        header = {
            "host": "datasearch.chinanpo.gov.cn",
            "Connection": "keep-alive",
            "Content-Length": "268",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Referer": "https://datasearch.chinanpo.gov.cn/gsxt/newList",
            "Origin": "https://datasearch.chinanpo.gov.cn",
            "Content-Type": "application/json;charset=UTF-8",
        }
        form = {
            "pageNo":"1",
            "pageSize":"10",
            "paramsValue":self.orgName,
            "ssfw":"1",
        }
        url = 'https://datasearch.chinanpo.gov.cn/gsxt/PlatformSHZZFRKGSXT/biz/ma/shzzgsxt/a/gridQuery.html'
        resp = postContent(url=url,headers=header,payload=json.dumps(form)).get("result")
        if isinstance(resp,dict):
            dataList = resp.get("data")
            for i in dataList:
                if isinstance(i,dict):
                    OrgID = i.get("aaae0102")
                    return OrgID
                else:
                    print("获取到的数据格式错误")
        else:
            print("{},获取到的数据格式错误".format(self.orgName))
    def getBaseInfo(self):
        payload = {
            "id":self.getOrgId()
        }
        headers = {
            "Host":"datasearch.chinanpo.gov.cn",
            "Connection":"keep-alive",
            "Content-Length":"27",
            "Accept":"application/json, text/plain, */*",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
            "Origin":"https://datasearch.chinanpo.gov.cn",
            "Referer":"https://datasearch.chinanpo.gov.cn/gsxt/newDetails?b="+(base64.b64encode(str(payload).encode("utf-8")).decode("utf-8")),
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Content-Type":"application/json;charset=UTF-8",
        }

        url = 'https://datasearch.chinanpo.gov.cn/gsxt/PlatformSHZZFRKGSXT/biz/ma/shzzgsxt/a/getAae01CertificateInfo.html'
        resp = postContent(url=url,headers=headers,payload=json.dumps(payload))
        print(resp)
        result = resp.get("result")

        if isinstance(result,dict):
            addr = result.get("aaae0116")
            orgCode = result.get("aaae0102")
            legalPerson = result.get("aaae0113")
            auth = result.get("aaae0107")
            cover = result.get("aaae0122")
            startTime = result.get("aaae0123")
            platformType = "YLXY"
            STATE = "10A"
            verifyFrom = result.get("aaae0703")
            verifyTo = result.get("aaae0704")
            Message = (self.orgName,addr,orgCode,legalPerson,auth,cover,startTime,platformType,STATE,self.orgName)
            self.insertToDB(data=Message)
        else:
            print("没有搜索到{}".format(self.orgName))


    def insertToDB(self,data):
        db = pymysql.connect(host='192.168.2.23', user='ch_data_oper', passwd='123456', db='db_store', port=7865)
        cursor = db.cursor()
        sql = 'UPDATE  c_basic_info Set ENTERPRISE_NAME=%s,REGISTERED_ADDRESS=%s,USCC=%s,LEGAL_PERSON=%s,REGISTRATION_AUTHORITY=%s,BUSINESS_SCOPE=%s,FOUNDED_DATE=%s,PLATFORM_TYPE=%s,STATE=%s' \
              ' where ENTERPRISE_NAME=%s'
        cursor.execute(sql,data)
        db.commit()
        db.close()
        print("{},该公司信息更新完成".format(self.orgName))
        return None






if __name__ == '__main__':
    comList = ["福州市国德老年康养中心",'福清音西夕阳乐乐乐之家','福州市西园老年公寓','福州市鼓楼区金太阳老年公寓','福州市长乐区古槐镇董奉山老年公寓',
               '福州市仓山区金浦老人公寓','闽侯县玖玖养老护理院','闽侯重阳养老院','福州市仓山区福海老龄公寓','福州市长乐区康佳老年公寓','连江县琯头镇侨兴老年公寓',
               '福州市仓山区栢林老年公寓','福州市仓山区百龄安养院','罗源县社会福利中心','罗源县爱心护老院','福州市台江区老人公寓']
    for comName in comList:
        g = getChinanpo(comName)
        g.getBaseInfo()

# 福州市社会福利院，闽侯县社会福利中心,福建省万友护养中心（福建医大附一护养中心）,永泰县金太阳老年公寓（永泰县社会福利中心）