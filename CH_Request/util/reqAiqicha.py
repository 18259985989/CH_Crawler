import os
import sys
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(dir_path)

from CH_Request.util.proxyPool import proxyPool as Proxy



class reqContent(object):
    """
    爱企查专用访问接口
    """
    def __init__(self,url,headers,payload):
        self.url = url
        self.headers = headers
        self.payload = payload
        self.errCount = 0
        self.flag = "Fail"
        self.proxy = Proxy()

    def reqJson(self):
        """
        通用Json格式请求
        :return:
        """
        while True:
            if self.errCount<5:
                try:
                    Ip = self.proxy.reqProxy()
                    resp = requests.get(url=self.url,headers=self.headers,params=self.payload,proxies={"https":Ip},timeout=10,verify=False)
                except Exception as e:
                    self.errCount += 1
                    print("请求内容中出现异常")
                else:
                    if resp.status_code != 200:
                        self.errCount += 1
                        print("请求公司Id时状态码不为200.")
                    else:
                        respJson = resp.json()
                        if isinstance(respJson,dict):
                            status = respJson.get("status")
                            if status == 0:
                                self.errCount = 0
                                return respJson
                            else:
                                self.errCount+=1
                        else:
                            self.errCount+=1
            else:
                return self.flag