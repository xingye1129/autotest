# -*- coding: UTF-8 -*-
import logging
import time
import datetime

path = '.'
logger = None
#create logger,输出到日志文件
#设置输出的格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt = '%Y-%m-%d %H:%M:%S')
# now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
#设置以追加的形式写入到日志文件
#打印到固定log文件中
c = logging.FileHandler(path + "/lib/logs/all.log",mode= 'a',encoding='utf8')
#加时间戳的文件中
# c = logging.FileHandler(path + "/lib/logs/" + now + "log.log",mode= 'a',encoding='utf8')
logger = logging.getLogger()
#输出日志等级开关
logger.setLevel(logging.INFO)
c.setFormatter(formatter)
#将logger添加到handler里面
logger.addHandler(c)


#将日志输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

#打印debug级别的日志

def debug(ss):
    global logger
    try:
        logging.debug(ss)
    except:
        return

#打印info级别的日志
def info(str):
    try:
        logging.info(str)
    except:
        return
#打印warn级别的日志
def warning(ss):
    try:
        logging.warning(ss)
    except:
        return
# 打印warn级别的日志
def error(ss):
    try:
        logging.error()
    except:
        return

#打印异常信息
def exception(e):
    try:
        logging.exception(e)
    except:
        return

#调试
if __name__=='__main__':
    debug('ssss')
    info('2222')
    warning('sdsdsd')
    exception('wewew')
    a = 1
    try:
        print(1 +'2')
    except Exception as e:
        exception(e)
