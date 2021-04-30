# -*- coding: utf-8 -*-
# @Time : 2021/01/25 14:27
# @Author :  Meow_J

import threading
import time
from CH_Request.function.getCreditChina import getCreditChina
from CH_Request.function.getCreditFuZhou import CreditFuZhou
import sys

sys.path.append('/extdisk/home/chenghua_spider')

from rabbitMQ.rabbitMQ import RabbitMQ
from rabbitMQ.rabbitMQQueue import RabbitMQQueueEnum
from rabbitMQ.rabbitMQMonitor import RabbitMQMonitor
from rabbitMQ.consumer import runConsumer
# from crawlerDocuments.Shuidi.SDXY_Main import SDXY
# from crawlerDocuments.QccReqEdition.QccSpider.QccMain import QccReqEdition
from CH_Request.function.getAiqicha import getAiqicha
import time

rabbitMQ = RabbitMQ()
rabbitMQMonitor = RabbitMQMonitor()
# 获取当前爬虫数，分配爬虫source 如 SOURCE_TYC = 52
crawler_source = rabbitMQMonitor.get_crawl_source(QUEUE_NAME='direct.passEx.DATA_MINING')
# field_time_name = 'shuidi_time'  # XXX_time修改 mytest.business_directory 中添加的更新时间字段
field_time_name_2 = 'qcc_time'# 用于更新时间检查  暂不修改


def start(rabbitMQ, source, message, pri):
    print(message)
    print(source)
    # XXX 修改为 新增爬虫的类，修改爬虫入口方法名为 run
    runConsumer(getAiqicha, rabbitMQ, message, pri, field_time_name_2, crawler_source)

def dealDeadMessage(rabbitMQ, source, message, pri, fromqueue):
    # 如果消息优先级大于0，即重新发送到爬取队列中
    print('dead meassage', message)
    if pri > 0:
        time.sleep(10)
        rabbitMQ.sendMessagefullName(fromqueue, message, pri, source)
        rabbitMQ.logger.logger.info(
            'dead message from %s pri %s transmit to TOPIC_CRAWLER from %s' % (fromqueue, str(pri), message))
        return
    rabbitMQ.logger.logger.info('dead message from %s pri %s is lowest , discard message' % (fromqueue, str(pri)))

if __name__ == '__main__':
    QUEUE_NAME = 'QCC_Na'  # 声明爬虫的队列名 例如天眼查（TYC），如此队列是需要整合的队列 队列名该声明为 XXX_Na
    QUEUE_NAME_QCC = 'qcc_req'

    THREAD_NUM = 4 # 声明该爬虫的线程数量

    # 如果需要申明队列长度(可选)
    QUEUE_LIMIT = 20

    # 添加死信消息的转发(可选)
    DEAD_LETTER_NAME = 'message'
    DEAD_LETTER_NUM = 2
    DEAD_EXCHANGE = 'dead'  # (暂时不需更改)
    # rabbitMQ.addRelativeTopic(topicName=DEAD_EXCHANGE, queueName=DEAD_LETTER_NAME, threadNum=DEAD_LETTER_NUM,
    #                           callback=dealDeadMessage)#需要死信消息的时候开启

    # rabbitMQ.addRelativeTopic(topicName=RabbitMQQueueEnum.TOPIC_CRAWLER, queueName=QUEUE_NAME, threadNum=THREAD_NUM,
    #                           callback=start)#不需要队列长度和死信消息

    # rabbitMQ.addRelativeTopic(topicName=RabbitMQQueueEnum.TOPIC_CRAWLER, queueName=QUEUE_NAME, threadNum=THREAD_NUM,
    #                           callback=start, queueLimit=QUEUE_LIMIT)  # 只需要队列长度

    # rabbitMQ.addRelativeTopic(topicName=RabbitMQQueueEnum.TOPIC_CRAWLER, queueName=QUEUE_NAME_LD, threadNum=THREAD_NUM,
    #                           callback=start_ld, queueLimit=QUEUE_LIMIT)

    rabbitMQ.addRelativeQueue(queueName=RabbitMQQueueEnum.QUEUE_DATA_MINING, threadNum=THREAD_NUM,
                              callback=start)#需要队列长度和死信消息

    rabbitMQ.startRabbitMq()



# 创建新线程
# if __name__ == '__main__':
#     comName = "福建巨麦文化传媒有限公司"
#     thread1 = getCreditChina(comName)
#     thread2 = CreditFuZhou(comName)
#
#     # 开启新线程
#     thread1.start()
#     thread2.start()
#     thread1.join()
#     thread2.join()
#     print ("退出主线程")


