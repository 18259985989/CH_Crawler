#!/usr/bin/python
# -*- coding: UTF-8 -*-

from rabbitMQ.rabbitMQConn import RabbitMQConn
from rabbitMQ.rabbitMQQueue import RabbitMQQueue, RabbitMQQueueEnum
from rabbitMQ.rabbitMQMonitor import RabbitMQMonitor
from rabbitMQ.logger import Logger

THREAD_NUM = 'threadNum'
CALLBACK = 'callback'
QUEUE_NAME = 'queueName'
TOPIC_NAME = 'topicName'
RABBITMQ = 'rabbitMQ'
SEND_QUEUE = 'sendQueue'
QUEUE_LIMIT = 'queueLimit'
DEAD_LETTER_NAME = 'deadLetterName'
DEAD_EXCHANGE = 'deadExchange'


class RabbitMQ():
    def __init__(self):
        self.logger = Logger(__name__)
        self.queueInfoMap = {}
        self.topicInfoMap = {}
        self.rabbitMQMonitor = None
        self.sendRabbitMQ = None

    # 添加关注队列对象, 默认单线程, 发送队列时, 可不填后两个参数
    def addRelativeQueue(self, queueName, threadNum=1, callback=None, queueLimit=None, deadExchange=None,
                         deadLetterName=None):
        tmpRelativeInfo = {}
        tmpRelativeInfo[THREAD_NUM] = threadNum
        tmpRelativeInfo[CALLBACK] = callback
        tmpRelativeInfo[QUEUE_LIMIT] = queueLimit
        tmpRelativeInfo[DEAD_EXCHANGE] = deadExchange
        tmpRelativeInfo[DEAD_LETTER_NAME] = deadLetterName
        if self.queueInfoMap.get(queueName) is not None:
            self.logger.logger.warning(
                "queue[" + queueName + "] has been already registered, this operate will cover it.")
        self.queueInfoMap[queueName] = tmpRelativeInfo
        self.logger.logger.debug("add relative queue[%s] success." % queueName)

    def addRelativeTopic(self, topicName, queueName=None, threadNum=1, callback=None, queueLimit=None,
                         deadExchange=None,
                         deadLetterName=None):
        tmpRelativeInfo = {}

        # 表示关注默认队列
        if callback is not None and queueName is None:
            queueName = "default"

        tmpRelativeInfo[THREAD_NUM] = threadNum
        tmpRelativeInfo[CALLBACK] = callback
        tmpRelativeInfo[QUEUE_NAME] = queueName

        tmpRelativeInfo[TOPIC_NAME] = topicName
        tmpRelativeInfo[QUEUE_LIMIT] = queueLimit
        tmpRelativeInfo[DEAD_EXCHANGE] = deadExchange
        tmpRelativeInfo[DEAD_LETTER_NAME] = deadLetterName

        if queueName is not None:
            topicKey = topicName + queueName
        else:
            topicKey = topicName

        if self.topicInfoMap.get(topicKey) is not None:
            self.logger.logger.warning(
                "topic[" + topicName + "] has been already registered, this operate will cover it.")
        self.topicInfoMap[topicKey] = tmpRelativeInfo
        self.logger.logger.debug("add relative topic[%s] success." % topicName)

    def recvRabbitMQ(self, relativeInfoMap):
        for name, info in relativeInfoMap.items():
            info[RABBITMQ].startRecv()

    # 有接收的时候会阻塞
    def startRabbitMq(self):
        # 每个队列和主题进行连接
        for queueName, info in self.queueInfoMap.items():
            name = RabbitMQQueue.getQueueName(None, queueName)
            info[RABBITMQ] = RabbitMQConn(None, name, info[THREAD_NUM], info[CALLBACK], self, info[QUEUE_LIMIT],
                                          info[DEAD_EXCHANGE],
                                          info[DEAD_LETTER_NAME])
            info[RABBITMQ].startConnect()
            if self.sendRabbitMQ is None and info[CALLBACK] is None:
                self.sendRabbitMQ = info[RABBITMQ]
            self.logger.logger.debug("start recv queue[%s] with %s threads." % (name, info[THREAD_NUM]))

        for topicKey, info in self.topicInfoMap.items():
            if info[QUEUE_NAME] is not None:
                name = RabbitMQQueue.getQueueName(info[TOPIC_NAME], info[QUEUE_NAME])
            else:
                name = info[QUEUE_NAME]
            info[RABBITMQ] = RabbitMQConn(info[TOPIC_NAME], name, info[THREAD_NUM], info[CALLBACK], self,
                                          info[QUEUE_LIMIT], info[DEAD_EXCHANGE],
                                          info[DEAD_LETTER_NAME])
            info[RABBITMQ].startConnect()
            if self.sendRabbitMQ is None and info[CALLBACK] is None:
                self.sendRabbitMQ = info[RABBITMQ]
            self.logger.logger.debug("start recv topic[%s] with %s threads." % (info[TOPIC_NAME], info[THREAD_NUM]))

        # 开始接收消息
        self.recvRabbitMQ(self.queueInfoMap)
        self.recvRabbitMQ(self.topicInfoMap)

    def getSendRabbitMQ(self):
        if self.sendRabbitMQ is None:
            # 只是用来发送
            self.sendRabbitMQ = RabbitMQConn(None, RabbitMQQueue.getQueueName(None, SEND_QUEUE))
            self.sendRabbitMQ.startConnect()

        return self.sendRabbitMQ

    def sendMessage(self, queueName, message, prio=RabbitMQQueueEnum.PRIO_LOW, source=0):
        # 同一个队列不能自发自收
        name = RabbitMQQueue.getQueueName(None, queueName)
        self.getSendRabbitMQ().sendMessage(name, message, prio, source)

    def sendMessagefullName(self, queueName, message, prio=RabbitMQQueueEnum.PRIO_LOW, source=0):
        # 同一个队列不能自发自收

        self.getSendRabbitMQ().sendMessage(queueName, message, prio, source)

    def publishMessage(self, topicName, message, prio, source=0):
        # 任意topic的Mq都可以发布
        self.getSendRabbitMQ().publishMessage(topicName, message, prio, source)

    def getQueueMessageCount(self, queueName):
        if self.rabbitMQMonitor is None:
            self.rabbitMQMonitor = RabbitMQMonitor()

        name = RabbitMQQueue.getQueueName(None, queueName)
        return self.rabbitMQMonitor.get_messages(name)
