# 政府采购网站
# -*- coding: utf-8 -*-
# @Time : 2021/04/06 10:27
# @Author :  Meow_J

import requests
from PIL import Image
from io import BytesIO
from hashlib import md5

class GovProcurement(object):

    def __init__(self):
        pass

    def ReqContent(self):
        url = 'http://www.ccgp-fujian.gov.cn/3500/noticelist/e8d2cd51915e4c338dc1c6ee2f02b127/'
        headers = {
            "Host":"www.ccgp-fujian.gov.cn",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
        }
        res = requests.get(url=url, headers=headers, timeout=20, verify=False)
        text =  res.text
        if "请完成上方验证码操作" in text:
            print("出现验证码")

        else:
            pass

    def reqPic(self):
        url = 'http://www.ccgp-fujian.gov.cn/noticeverifycode/'
        headers = {
            "Host": "www.ccgp-fujian.gov.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "keep-alive",
            "Referer": "http://www.ccgp-fujian.gov.cn/3500/noticelist/e8d2cd51915e4c338dc1c6ee2f02b127/",
        }
        payload = {
            "1":""
        }
        response = requests.get(url=url,headers=headers,params=payload,timeout=20,verify=False)
        f = BytesIO(response.content)
        img = Image.open(f)
        img.save(r'C:\Users\Administrator\Desktop\Crawler\CH_Crawler\CH_Request\function\code_img.png')
        print('验证码图片刷新完成')

    def recognition_image_verification_code(self):
        img = open(r'C:\Users\Administrator\Desktop\Crawler\CH_Crawler\CH_Request\function\img\code_img.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        res = CJY.PostPic(img, 2004)
        print(res)
        data = res.get('pic_str')
        return data


#第三方接码平台
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


if __name__ == '__main__':
    g = GovProcurement()
    CJY = Chaojiying_Client('a8809007', 'a472189859', '901568')
    # g.recognition_image_verification_code()

    # import uuid
    # a = str(uuid.uuid4())
    # print(a.replace("-",""))

    # import hashlib
    # a = "mj"
    # print(hashlib.md5(a.encode(encoding='utf-8')).hexdigest())

    print()