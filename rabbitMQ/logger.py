import logging
import datetime
import os

class Logger:
    #默认打印info, 记录info、error
    def __init__(self, module):
        consoleLevel = logging.INFO
        logInfoFile = 'info'
        logErrorFile = 'error'
        #当前路径下
        logPath = os.path.abspath('.') + "/logs/"
        if os.path.exists(logPath) == False:
            os.makedirs(logPath)

        #log加入日期, 记录info和error
        currentDate = datetime.datetime.now().strftime('%Y_%m_%d')
        logInfoFile = logPath + logInfoFile + "-" + currentDate + ".log"
        logErrorFile = logPath + logErrorFile + "-" + currentDate + ".log"

        self.logger = logging.getLogger(module)
        # 如果logger已有hander 则不再添加Logger
        if len(self.logger.handlers) > 0:
            return

        #定义log的接收级别, 保证所有log都收得到，必须定义为debug
        self.logger.setLevel(level = logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')

        #记录到文件的级别
        infohandler = logging.FileHandler(logInfoFile)
        infohandler.setLevel(logging.INFO)
        infohandler.setFormatter(formatter)
        self.logger.addHandler(infohandler)

        errorhandler = logging.FileHandler(logErrorFile)
        errorhandler.setLevel(logging.INFO)
        errorhandler.setFormatter(formatter)
        self.logger.addHandler(errorhandler)

        #输出到console的级别
        console = logging.StreamHandler()
        console.setLevel(consoleLevel)
        console.setFormatter(formatter)
        self.logger.addHandler(console)
