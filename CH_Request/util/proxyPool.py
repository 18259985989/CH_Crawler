# -*- coding: utf-8 -*-
# @Time : 2021/4/14 21:19
# @Author :  Meow_J

"""
代理池管理（快代理）
"""

import requests
import json
from datetime import datetime
from threading import Timer

class proxyPool(object):

    def __init__(self):
        self.orderId = '921967806545863' #订单号
        self.getNums = 30    #可选大小 1-100(为了保证Ip质量一般不取太大，取太大很多都是重复的)
        self.flag = "Fail"

    def reqProxy(self):
        """
        请求链接获取代理
        :return:
        """
        # task = Timer(5, self.reqProxy)
        # url = 'http://dev.kdlapi.com/api/getproxy/'
        url = 'http://svip.kdlapi.com/api/getproxy/'
        payload = {
            "orderid":self.orderId,
            "num":self.getNums,
            "protocol":2,
            "format":"json",
            "sep":"1",
            "an_ha":"1",
            "method":"1",
            "quality":"2", #svip为2  vip为1
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Host": "dev.kdlapi.com",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        }
        resp = requests.get(url=url,headers=headers,params=payload)
        result = json.loads(resp.text)
        try:
            proxy_list = result.get("data").get("proxy_list")
            # print(proxy_list)
        except Exception as e:
            print("获取代理列表时出现异常。{}".format(e))
        else:
            for proxy in proxy_list:
                res = self.checkProxy(proxy=proxy)
                if res != self.flag:
                    print("获取到代理为：{}。--{}".format(proxy,datetime.now()))
                    # task.start()
                    return proxy
                else:
                    continue

    def checkProxy(self,proxy):
        """
        检测获取到的ip是否可用
        :return:
        """
        url = 'https://www.baidu.com/'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
        }
        try:
            resp = requests.get(url=url,headers=headers,proxies={"https":proxy},timeout=5)
        except Exception as e:
            print("请求超时，更换Ip")
            return self.flag
        else:
            if resp.status_code != 200:
                print("返回结果异常")
                return self.flag
            else:
                return proxy


if __name__ == '__main__':
    p = proxyPool()
    p.reqProxy()
