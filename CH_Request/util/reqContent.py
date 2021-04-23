import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def reqContent(url,headers,payload):
    try:
        res = requests.get(url=url,headers=headers,params=payload,timeout=20,verify=False)
    except Exception as e:
        print(e)
    else:
        if res.status_code != 200:
            print(res.status_code)
        else:
            result = res.json()
            return result

def postContent(url,headers,payload):
    try:
        res = requests.post(url=url,headers=headers,data=payload,timeout=20,verify=False)
    except Exception as e:
        print(e)
    else:
        if res.status_code != 200:
            print(res.status_code)
        else:
            result = res.json()
            return result

