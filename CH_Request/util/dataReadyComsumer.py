# -*- coding: utf-8 -*-
# @Time : 2021/4/28 14:09
# @Author :  Meow_J

import sys

sys.path.append('/extdisk/home/chenghua_spider')
from rabbitMQ.rabbitMQ import RabbitMQ
from rabbitMQ.rabbitMQQueue import RabbitMQQueueEnum
from rabbitMQ.rabbitMQQueue import RabbitMQSourceEnum
from rabbitMQ.rabbitMQMonitor import RabbitMQMonitor
from CH_Request.util.SQLAlchemy.databaseService import DatabaseService

from rabbitMQ.logger import Logger
import threading
import json
import time
from CH_DB.fetchDataBase import *
from CH_Request.util.dataggregateFileTest import DAF
import traceback
import uuid


class RequirementService:
    def __init__(self):
        self.rabbitMQ = RabbitMQ()
        self.thread = None
        self.logger = Logger(__name__)
        # self.databaseService = DatabaseService("192.168.10.68", "3306", "root", "123456", "dataggregate")

        # 需求来源暂时是两个, 后台系统和企业名录, 本身只做转发和查询, 暂时不需要多线程
        self.rabbitMQ.addRelativeQueue(RabbitMQQueueEnum.QUEUE_DATA_READY, 1, self.searchReqProcess)

        # 根据需求源，回复不同的队列
        # self.rabbitMQ.addRelativeQueue(RabbitMQQueueEnum.QUEUE_ASRESP)
        # self.rabbitMQ.addRelativeQueue(RabbitMQQueueEnum.QUEUE_CISPRESP)
        # self.rabbitMQ.addRelativeQueue(RabbitMQQueueEnum.QUEUE_TIMECLOCK)
        #
        # # 添加死信消息的转发
        # self.rabbitMQ.addRelativeTopic(RabbitMQQueueEnum.TOPIC_DEAD, RabbitMQQueueEnum.QUEUE_DEAD, 2,
        #                                self.dealDeadMessage)
        #
        # # 发消息队列，只需要关注
        # # 关注爬虫TOPIC
        # self.rabbitMQ.addRelativeTopic(RabbitMQQueueEnum.TOPIC_CRAWLER)

    def startRecv(self):
        self.thread = threading.Thread(target=self.rabbitMQ.startRabbitMq)
        self.thread.start()


    # 分发给爬虫进程进行爬取
    def searchReqProcess(self, rabbitMQ,source, message, pri):
        # 暂时时效性不做单独处理
        print(message)
        print(type(message))
        try:
            jsonData = json.loads(message)
        except:
            jsonData = json.loads(message[2:])
        print(jsonData)
        if "o_pay_info_id" not in jsonData.keys():
            result = get_uscc_from_basic_info(jsonData)
            jsonData["o_pay_info_id"] = None
        else:
            result = get_uscc_from_o_pay_info(jsonData)
        print(result)

        companyName = result["COMPANY_NAME"]
        scode = result["COMPANY_USCC"]
        self.logger.logger.info("search Company[%s], scode[%s]." % (companyName, scode))
        # 暂时定义为一个月内有效
        # expireDay = 30
        # time.sleep(20)
        callpro()
        if jsonData["o_pay_info_id"] is None:
            self.logger.logger.info('already in database %s' % str(jsonData))
            return

        companyInfo = DAF(result).getDataFromDbStore(jsonData["o_pay_info_id"])
        report_id = str(uuid.uuid1())
        report_id = report_id.replace("-", "")
        print(companyInfo)
        try:
            while True:
                if companyInfo:
                    if jsonData["o_pay_info_id"] is not None or jsonData["o_pay_info_id"] is not "":
                        update_credit_report_info(result)
                        insert_result = insert_credit_report_info(report_id, result, companyInfo)
                        if insert_result == 1:
                            jsonData["credit_report_info_id"] = report_id
                            # rabbitMQ.sendMessage(RabbitMQQueueEnum.QUEUE_GEN_REPORT, str(jsonData))
                            self.logger.logger.info('already in database send %s to QUEUE_GEN_REPORT' % str(jsonData))
                            if jsonData["o_pay_info_id"] is not None or jsonData["o_pay_info_id"] != "":
                                update_order_status(jsonData["o_pay_info_id"])
                            return
                    else:
                        self.logger.logger.info('already in database send %s to QUEUE_GEN_REPORT' % str(jsonData))

                else:
                    time.sleep(20)
                    companyInfo = DAF(result).getDataFromDbStore(jsonData["o_pay_info_id"])
            # 来自应用系统的需求, 优先级最高, 直接转发
            self.logger.logger.info(
                "recv [%s] from application system, high prio publish." % (message))


        except:
            self.logger.logger.error(traceback.format_exc())


if __name__ == '__main__':
    rqu = RequirementService()
    rqu.startRecv()
