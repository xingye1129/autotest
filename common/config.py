from common import logger
from common.Txt import Txt


#定义全局变量用来存储配置文件读取后，保存为键值对格式文件
config = {}



def get_config(path):
    """
    powered by Mr Will
    at 2018-12-22
    用来格式化打印日志到文件和控制台
    :param path:配置文件路径
    :return:返回配置文件dict
    """
    global config
    # 重新获取时，先清空配置
    config.clear()
    txt = Txt(path)
    data = txt.read()
    #打印按行读取到的文件内容
    # print(data)
    for s in data:
        # 跳过注释
        if s.startswith('#'):
            continue

        if not s.find('=') > 0:
            logger.warn('配置文件格式错误，请检查：' + str(s))
            continue

        try:
            #获取key的值
            key = s[0:s.find('=')]
            #获取值
            value = s[s.find('=') + 1:s.__len__()]
            #使config列表的key=value
            config[key] = value
        except Exception as e:
            logger.warn('配置文件格式错误，请检查：' + str(s))
            logger.exception(e)
    return config

#调试代码，打印txt转化为键值对的列表
# get_config(path='../conf/conf.properties')
# print(config)
