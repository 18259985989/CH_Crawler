# -*- coding: utf-8 -*-
# @Time : 2021/01/25 14:27
# @Author :  Meow_J

import threading
import time
from CH_Request.function.getCreditChina import getCreditChina
from CH_Request.function.getCreditFuZhou import CreditFuZhou

# 创建新线程
if __name__ == '__main__':
    comName = "福建巨麦文化传媒有限公司"
    thread1 = getCreditChina(comName)
    thread2 = CreditFuZhou(comName)

    # 开启新线程
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    print ("退出主线程")


