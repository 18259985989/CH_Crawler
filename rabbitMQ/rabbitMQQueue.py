from enum import Enum, unique


class RabbitMQQueue:
    AMQ = 'amq'
    TOPIC_STR = "fanout"
    QUEUE_STR = "direct"
    PASSEX_STR = "passEx"
    DEADEX_STR = "DEADex"

    def getQueueName(topic=None, queue=None):
        if topic is not None:
            queueName = "%s.%s.%s" % (RabbitMQQueue.TOPIC_STR, topic, queue)
        else:
            queueName = "%s.%s.%s" % (RabbitMQQueue.QUEUE_STR, RabbitMQQueue.PASSEX_STR, queue)

        return queueName


class RabbitMQQueueEnum:
    QUEUE_SEARCHREQ = "SearchReqB"
    QUEUE_ASRESP = "ASResp"
    QUEUE_BDRESP = "BDResp"
    QUEUE_DAGR = 'DAGResp'
    QUEUE_CISPRESP = 'CispResp'
    QUEUE_TIMECLOCK = 'TIMECLOCK'
    QUEUE_TEST1 = "test1"
    QUEUE_TEST2 = "test2"
    QUEUE_TYC = 'TYC'
    QUEUE_GSXT = 'GSXT_Na'
    QUEUE_BZXR = 'BZXR_Na'
    QUEUE_FYGG = 'FYGG_Na'
    TOPIC_CRAWLER = "crawler"
    TOPIC_Test = "queueTest"
    TOPIC_DEAD = 'dead'
    QUEUE_DEAD = 'message'
    QUEUE_COMBINE = 'combine'
    QUEUE_TEST = 'TEST'

    QUEUE_DATA_MINING = 'DATA_MINING'

    # QUEUE_TEST2
    PRIO_MOST = 3
    PRIO_HIGH = 2
    PRIO_NORMAL = 1
    PRIO_LOW = 0


@unique
class RabbitMQSourceEnum(Enum):
    SOURCE_ASREQ = 1
    SOURCE_BDREQ = 2

    SOURCE_GSXT = 51
    SOURCE_TYC = 52
    SOURCE_BZXR = 54
    SOURCE_FYGG = 58

    SOURCE_FROM = 'fromApp'
