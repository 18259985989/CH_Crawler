import configparser
import os
import requests
import json
from urllib.parse import quote
import math
from rabbitMQ.logger import Logger
import traceback
from retrying import retry
import time


class RabbitMQMonitor:
    def __init__(self):
        self.readConfig()
        self.logger = Logger(__name__)

    def readConfig(self):
        # 读取配置文件
        cf = configparser.ConfigParser()
        # TBD: 目录调整
        cf.read(os.path.dirname(os.path.abspath(__file__)) + "/config.conf")
        # 读取配置信息
        self.host = cf.get("rabbitMQ", "host")
        self.username = cf.get("rabbitMQ", "username")
        self.password = cf.get("rabbitMQ", "password")
        self.mngPort = cf.get("rabbitMQ", "mngPort")
        self.vhost = cf.get("rabbitMQ", "vhost")

    @retry(stop_max_attempt_number=1000)
    def get_messages(self, queueName):
        try:
            url = 'http://%s:%s/api/queues/%s/%s' % (self.host, self.mngPort, quote(self.vhost, 'utf-8'), queueName)
            resp = requests.get(url, auth=(self.username, self.password))
            if resp.status_code != 200:
                return -1
            dic = json.loads(resp.text)
        except:
            self.logger.logger.error(traceback.format_exc())
            time.sleep(60)
            raise Exception
        return dic['messages_ready'], dic['messages_unacknowledged'], dic['consumers']

    def get_crawler_queue_num(self):
        url = 'http://%s:%s/api/queues/%s' % (self.host, self.mngPort, quote(self.vhost, 'utf-8'))
        resp = requests.get(url, auth=(self.username, self.password))
        if resp.status_code != 200:
            return -1
        dic = json.loads(resp.text)
        index = 0
        for me in dic:
            # 前缀为fanout.crawler 为爬虫队列，且当该爬虫队列存在消费者的情况下
            if 'fanout.crawler' in me['name'] and me['consumers'] > 0:
                if '_Na' in me['name'] or 'TYC' in me['name']:  # 即为需要整合的队列
                    index += 1
        return index

    def get_bitmap_num(self):
        num = self.get_crawler_queue_num()
        k = 0
        for i in range(num):
            k += math.pow(2, i)
        return int(k)

    def get_crawl_source(self, QUEUE_NAME):
        if "_Na" not in QUEUE_NAME:
            return 0
        n = self.get_crawler_queue_num()
        if n != -1:
            return int(50 + math.pow(2, n))
        else:
            self.logger.logger.error("can't get crawler_queue_num ,check  rabbitmq's status")
            return None

    def get_crawl_unacknowledged(self):
        url = 'http://%s:%s/api/queues/%s' % (self.host, self.mngPort, quote(self.vhost, 'utf-8'))
        resp = requests.get(url, auth=(self.username, self.password))
        if resp.status_code != 200:
            return -1
        dic = json.loads(resp.text)
        index = 0
        for me in dic:
            # 前缀为fanout.crawler 为爬虫队列，且当该爬虫队列存在消费者的情况下
            if 'fanout.crawler' in me['name'] and me['consumers'] > 0:
                if me['messages_unacknowledged'] == 0:
                    index += 1
        return index

    def get_crawl_ready(self):
        url = 'http://%s:%s/api/queues/%s' % (self.host, self.mngPort, quote(self.vhost, 'utf-8'))
        resp = requests.get(url, auth=(self.username, self.password))
        if resp.status_code != 200:
            return -1
        dic = json.loads(resp.text)
        index = 0
        for me in dic:
            # 前缀为fanout.crawler 为爬虫队列，且当该爬虫队列存在消费者的情况下
            if 'fanout.crawler' in me['name'] and me['consumers'] > 0:
                if me['messages_ready'] == 0:
                    index += 1
        return index


if __name__ == '__main__':
    r = RabbitMQMonitor()
    print(r.get_crawler_queue_num())
    print(r.get_crawl_unacknowledged())
    # print(r.get_messages())
