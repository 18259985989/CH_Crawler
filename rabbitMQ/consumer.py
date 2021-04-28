import json
import traceback

import pymysql

from rabbitMQ.logger import Logger
from rabbitMQ.rabbitMQQueue import RabbitMQSourceEnum, RabbitMQQueueEnum


def ifExist(company, fromtime):
    conn = pymysql.connect(host='192.168.2.23', user='ch_data_source', passwd='123456', db='db_source',port=7865)
    cursor = conn.cursor()
    # sql = 'select company from business_directory b where b.company=%s and ((to_days(now()) - to_days(b.' + fromtime + '))>30 or b.' + fromtime + ' is null) order by id desc'
    # sql = 'select company from business_directory b where b.id=%s and (b.' + fromtime + ' is null) order by id desc'
    sql = 'select Enterprise_name from base_info where Enterprise_name="{}" '.format(company)
    cursor.execute(sql,)
    res = cursor.fetchone()
    # print(res)
    if res:
        return True
    return True
def getUpper(crawltime):
    if isinstance(crawltime, str):
        crawltime = crawltime.replace('time', '')
        crawltime = crawltime.upper()
        return crawltime

def send_Break_info(rabbitMQ, message, crawl, value, error):
    search = json.loads(message)
    Logger(__name__).logger.error('%s %s breakdown' % (crawl, message))
    if RabbitMQSourceEnum.SOURCE_FROM.value in search:
        search['breakdown'] = crawl
        rabbitMQ.sendMessage(RabbitMQQueueEnum.QUEUE_DAGR, json.dumps(search), 1, value)
    Logger(__name__).logger.error(error)
def runConsumer(clas, rabbitmq, message, pri, crawltime, sourceValue):
    dataS = getUpper(crawltime)
    try:
        search = json.loads(message)
        search['id'] = 9746981
        flag = True
        cl = clas(search)
        Logger(__name__).logger.info('%s get message %s' % (dataS, message))
        if 'id' in search:
            if ifExist(search['id'], crawltime):
                cl.run()
                flag = False
                Logger(__name__).logger.info('%s %s crawl done' % (dataS, message))
                # updateCrawlTime(search['id'], crawltime)
        if pri == 2 and RabbitMQSourceEnum.SOURCE_FROM.value not in search:
            cl.run()
            flag = False
            Logger(__name__).logger.info('%s %s crawl done' % (dataS, message))
            # updateCrawlTime(search['id'], crawltime)
        if RabbitMQSourceEnum.SOURCE_FROM.value in search:
            if flag:
                cl.run()
                if sourceValue != 0:
                    rabbitmq.sendMessage(RabbitMQQueueEnum.QUEUE_DAGR, message, 1, sourceValue)
            Logger(__name__).logger.info('%s send %s to QUEUE_DAGR ' % (dataS, message))
    except:
        print(traceback.format_exc())
        send_Break_info(rabbitmq, message, dataS + 'Crawl', sourceValue, traceback.format_exc())