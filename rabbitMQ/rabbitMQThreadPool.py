import threading
from rabbitMQ.logger import Logger


# rabbitMQ 线程池
class RabbitMQThreadPool:
    def __init__(self, maxWorkers, channel):
        self.logger = Logger(__name__)
        self.maxWorkers = maxWorkers
        self.taskWorkers = 0
        self.semaphore = threading.Semaphore(maxWorkers)
        self.channel = channel

    def threadExecusor(self, func, *args):
        if func is not None:
            try:
                if len(args[0]) == 5:
                    func(args[0][0], int(args[0][1]), args[0][2], args[0][3], args[0][4])
                else:
                    # source需要做转换
                    func(args[0][0], int(args[0][1]), args[0][2], args[0][3])
            except Exception as e:
                source = args[0][1]
                msg = args[0][2]
                self.logger.logger.error("process message error. from source[%s], message:" % (source))
                self.logger.logger.error(msg)
                self.logger.logger.exception(e)

        self.semaphore.release()

    def submit(self, func, *args):
        self.semaphore.acquire()
        thread = threading.Thread(target=self.threadExecusor, args=(func, *args))
        thread.start()
