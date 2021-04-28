import pika
import configparser
import time
from rabbitMQ.rabbitMQThreadPool import RabbitMQThreadPool
from rabbitMQ.rabbitMQQueue import RabbitMQQueueEnum
import os
from rabbitMQ.logger import Logger
import threading


class RabbitMQConn:
    def __init__(self, topicName=None, queueName=None, threadNum=1, callback=None, master=None, queueLimit=None,
                 deadExchange=None,
                 deadLetterName=None):
        self.logger = Logger(__name__)
        self.readConfig()
        self.connection = None
        self.channel = None
        self.queueName = queueName
        self.topicName = topicName
        self.thread = None
        self.callback = callback
        self.threadNum = threadNum
        self.threadPool = None
        self.queue = None
        self.master = master
        # 引入信号量, 同一时刻, 一个rabbitMq只能执行一次send动作
        self.semaphore = threading.Semaphore(1)
        self.priority = 0
        self.queueLimit = queueLimit
        self.deadExchange = deadExchange
        self.deadLetterName = deadLetterName

    def readConfig(self):
        # 读取配置文件
        cf = configparser.ConfigParser()
        # TBD: 目录调整
        cf.read(os.path.dirname(os.path.abspath(__file__)) + "/config.conf")
        # 读取配置信息
        self.host = cf.get("rabbitMQ", "host")
        self.username = cf.get("rabbitMQ", "username")
        self.password = cf.get("rabbitMQ", "password")
        self.credentials = pika.PlainCredentials(self.username, self.password)
        self.port = cf.get("rabbitMQ", "port")
        self.vhost = cf.get("rabbitMQ", "vhost")
        self.retryIntval = cf.get("rabbitMQ", "retryIntval")
        self.maxPrio = cf.get("rabbitMQ", "maxPrio")
        self.maxLength = cf.get("rabbitMQ", "maxlength")

    def connect(self):
        # 连接rabbitMQ服务器
        try:
            parameter = pika.ConnectionParameters(self.host, self.port, self.vhost, self.credentials, heartbeat=0)
            self.connection = pika.BlockingConnection(parameter)
            self.logger.logger.debug("connect to server[%s:%s] success" % (self.host, self.port))
        except:
            # 连接失败, 重新读取文件
            self.readConfig()
            self.logger.logger.error("connect error, try to reconnect Server:" + self.host + ":" + self.port)
            time.sleep(self.retryIntval)
            self.connect()
        else:
            self.channel = self.connection.channel()

        return self

    def declareQueue(self):
        try:
            if self.queueLimit and self.deadLetterName:
                arguments = {'x-max-priority': int(self.maxPrio),
                             'x-dead-letter-exchange': self.deadExchange,
                             'x-dead-letter-routing-key': self.deadLetterName,
                             'x-max-length': self.queueLimit,
                             # 'x-overflow': "reject-publish"
                             }
            elif self.queueLimit and self.deadLetterName == None:
                arguments = {'x-max-priority': int(self.maxPrio), 'x-max-length': self.queueLimit}
            else:
                arguments = {'x-max-priority': int(self.maxPrio)}

            if self.topicName == "dead":
                arguments.pop("x-max-priority")
            self.queue = self.channel.queue_declare(queue=self.queueName, durable=True,
                                                    arguments=arguments)

            self.logger.logger.debug("declare queue [%s] success." % self.queueName)
        except Exception as e:
            self.logger.logger.error("declare queue[%s] error." % (self.queueName))
            self.logger.logger.exception(e)

    def declareTopic(self):
        if self.queueName is None:
            return
        try:
            self.declareQueue()
            exchange_type = 'fanout'
            self.topic = self.channel.exchange_declare(exchange=self.topicName, exchange_type=exchange_type)
            self.channel.queue_bind(exchange=self.topicName, queue=self.queueName, routing_key=self.queueName)
            self.logger.logger.debug("declare topic [%s] success." % self.topicName)
        except Exception as e:
            self.logger.logger.error("declare topic[%s] error." % (self.topicName))
            self.logger.logger.exception(e)

    def recvMessage(self):
        self.channel.basic_qos(prefetch_count=self.threadNum)
        self.channel.basic_consume(queue=self.queueName, on_message_callback=self.onMessage, auto_ack=False)
        self.channel.start_consuming()

    def onMessage(self, channel, method, properties, message):
        # 根据queue(routing_key)来查找回调
        messageData = message.decode('utf-8')
        messageSource = int(messageData[0:2])
        messageBody = messageData[2:]
        self.logger.logger.debug("recv message from [%s]." % messageSource)
        self.logger.logger.debug(messageBody)
        if self.threadPool is not None:
            # 死信转发到死信队列时，把死信来源队列名，添加到信息中转发
            if properties.headers and 'x-first-death-queue' in properties.headers:
                if properties.headers['x-first-death-queue']:
                    self.threadPool.submit(self.callback,
                                           (self.master, messageSource, messageBody, properties.priority,
                                            properties.headers['x-first-death-queue']))
            else:
                self.threadPool.submit(self.callback, (self.master, messageSource, messageBody, properties.priority))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def rabbitMQsendMesg(self, exchange, routingKey, message, priority, source):
        message = ('%02d' % (source)) + message
        self.logger.logger.debug("send message from [%s]." % source)
        self.logger.logger.debug(message)

        # 简单处理, 保证队列创建, 无需对应创建channel
        self.semaphore.acquire()
        if self.channel == None:
            self.channel = self.connection.channel()
        self.channel.basic_publish(exchange=exchange, routing_key=routingKey, body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                       priority=priority,
                                       content_encoding="utf-8"))
        self.semaphore.release()

    def sendMessage(self, queue, message, priority, source=0):
        # 发送给指定队列
        self.rabbitMQsendMesg('', queue, message, priority, source)

    def publishMessage(self, topic, message, priority, source=0):
        # 发送给指定交换机，但是不指定队列
        self.rabbitMQsendMesg(topic, '', message, priority, source)

    def startConnect(self):
        # 先进行连接
        self.connect()

        # 进行队列/主题申明
        if self.topicName is not None:
            self.declareTopic()
        else:
            self.declareQueue()

        # 开始队列接收
        if self.callback is None:
            return

        self.thread = threading.Thread(target=self.recvMessage)
        self.thread.start()
        # 开启线程池
        self.threadPool = RabbitMQThreadPool(self.threadNum, self.channel)

    def startRecv(self):
        if self.thread is not None:
            self.thread.join()

    def close(self):
        if self.thread is not None:
            self.thread.cancel()

        if self.connection is not None:
            self.connection.close()
