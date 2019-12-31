# -*- coding: UTF-8 -*-
import requests, json,traceback,urllib3
from common import logger
import jsonpath
from suds.client import Client
from suds.client import Client


class HTTP:
    """
        这是整个自动化框架接口模块关键字库
        powered by xingye
        at: 2019/11/19
    """

    def __init__(self,writer):
        self.session = requests.session()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.result = ''
        self.jsons = {}
        #用来保存关联数据字典
        self.params = {}
        #用来保存url
        self.url = ''
        self.writer = writer

    def seturl(self,u):
        """
         设置url的host地址
        :param u: url的host地址
        :return: 无
        """
        #判断读取到的参数是否为"http" 或者 "https"开头
        if u.startswith('http') or u.startswith('https'):
            self.url = u
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, self.url)
            return
        else:
            logger.error("ERRO: URL格式错误")
            self.writer.write(self.writer.row, 7, 'False')
            self.writer.write(self.writer.row, 8, 'URL格式错误')


    def get(self,url,params = None):
        """

        :param url:
        :param params:
        :return:
        """

        if not (url.startswith('http') or url.startswith('https')):
            url = self.url + '/' + url + '?' + params
        else:
            url = url + '?' + params

        res = self.session.get(url,verify=False)
        try:
            self.result = res.content.decode('utf8')
        except Exception as e:
            self.result = res.text
        logger.info(self.result)

        try:
            jsons = self.result
            jsons = jsons[jsons.find('{'):jsons.rfind('}') + 1]
            self.jsons = json.loads(jsons)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8,  str(self.jsons))
        except Exception as e:
            self.jsons = {}
            self.writer.write(self.writer.row, 7, 'False')
            self.writer.write(self.writer.row, 8,  str(self.jsons))






    def post(self,url,d=None,j=None):
        """
         发送post请求
        :param url:url路径，可以是全局的host路径+请求路径，也可以是以http,https开头的绝对请求路径
        :param d: 标准的url传参，date传参
        :param j: 传递json格式的参数
        :return:无
        """

        #用来读取的和host地址做拼接
        if not (url.startswith('http') or url.startswith('https')):
            url = self.url + '//' + url

        if d is None or d == '':
            pass
        else:
            d = self.__get_param(d)
            d = self.__getdate(d)

        try:
            #post请求
            re = self.session.post(url, d, j, verify=False)
        except Exception as e:
            re = e.__str__()


        if re is None or re=='error':
            self.result = re
        else:
            #用utf8格式提取字符传到result
            self.result = re.content.decode('UTF-8')

        logger.info(self.result)
        #转化为json格式字典形式
        try:
            self.jsons =json.loads(self.result)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.jsons))
        except Exception as e:
            self.jsons ={}
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8,  str(self.jsons))
            logger.exception(e)

    def removeheader(self,key):
        """
         从头里删除一个键值对
        :param key:要删除的键
        :return:无
        """
        try:
            self.session.headers.pop(key)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.session.headers))
        except Exception as e:
            logger.info("没有" + key + "这个键的header存在")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.session.headers))
            logger.exception(e)



    def addheader(self,key,value):
        """
         添加一个键值对，用来关联
        :param key: 要添加的键
        :param value:键的值
        :return:无
        """
        #从__get_param获取value，作为key的值
        value =self.__get_param(value)
        self.session.headers[key] = value
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, str(self.session.headers))

    def assertequals(self,key,value):
        '''
        断言json的结果里面，某个键的值和value相等
        :param key:json结果中的键
        :param value:预期的值
        :return:无
        '''
        value = self.__get_param(value)
        res = str(self.result)
        logger.info(self.jsons)
        try:
            res = str(jsonpath.jsonpath(self.jsons,str(key))[0])
        except Exception as e:
            logger.exception(e)

        if res == str(value):
            logger.info('PASS')
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.jsons))
        else:
            logger.info('FAIL')
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.jsons))

    def savejson(self,key,p):
        """
        将需要保存的数据，保存为参数p的值
        :param key: 需要保存的键的值
        :param p: 保存后，调用参数的参数名字{p}
        :return:无
        """
        try:
            self.params[p] = self.jsons[key]
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.params[p]))
        except Exception as e:
            logger.error('ERRO:没有' + key + '这个值')
            logger.exception(e)
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.jsons))

    def __get_param(self,s):
        #用传的参数，通过私有方法来替换为传的参数的值，并返回他的值，作为添加头中的值
        for key in self.params:
            s = s.replace('{' + key + '}',self.params[key])
        #返回替换后参数的值
        return s

    def __getdate(self,s):
        par ={}
        p = s.split('&')
        for ss in p:
            pp = ss.split('=')
            try:
                par[pp[0]] = pp[1]
            except Exception as e:
                logger.error('ERR0:参数错误！')
                logger.exception(e)
        return par


class SOAP():

    def __init__(self,writer):
        requests.packages.urllib3.disable_warnings()
        self.wsdl = ''
        self.client = None
        self.result = ''
        self.jsons = {}
        self.headers = {}
        self.params = {}
        self.url = ''
        self.writer=writer

    def adddoctor(self):
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, self.url)

    def setwsdl(self,url):
        self.url = url
        self.client = Client(url)
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, self.url)

    def callmethod(self,m, l):
        #调用服务并获得接口返回值
        l = l.split('、')
        if l == None or l ==['']:
            self.result = self.client.service.__getattr__(m)()
        else:
            for i in range(len(l)):
                l[i] = self.__get_param(l[i])
            self.result = self.client.service.__getattr__(m)(*l)

        try:
            jsons = self.result
            jsons = jsons[jsons.find('{'):jsons.rfind('}') + 1]
            self.jsons = json.loads(jsons)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.jsons))

        except Exception as e:
            self.jsons = {}
            self.writer.write(self.writer.row, 7, 'False')
            self.writer.write(self.writer.row, 8, str(self.jsons))

    #添加头
    def addheader(self,key,value):
        value = self.__get_param(value)
        self.headers[key]=value
        self.client = Client(self.url,headers=self.headers)
        self.writer.write(self.writer.row, 7, 'PASS')
        self.writer.write(self.writer.row, 8, str(self.headers))


    def removeheader(self,key):
        try:
            self.headers.pop(key)
            self.client = Client(self.url, headers=self.headers)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.headers))
        except Exception as e:
            logger.info("没有" + key + "这个键的header存在")
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.headers))
            logger.exception(e)


    def savejson(self,key,p):
        """
        将需要保存的数据，保存为参数p的值
        :param key: 需要保存的键的值
        :param p: 保存后，调用参数的参数名字{p}
        :return:无
        """
        try:
            if key not in self.jsons:
                pass
            else:
                self.params[p] = self.jsons[key]
            # print(self.jsons)
                self.writer.write(self.writer.row, 7, 'PASS')
                self.writer.write(self.writer.row, 8, str(self.params[p]))
        except Exception as e:
            logger.error('ERRO:没有' + key + '这个值')
            # logger.exception(e)
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.params[p]))

    def __get_param(self,s):
        #用传的参数，通过私有方法来替换为传的参数的值，并返回他的值，作为添加头中的值
        for key in self.params:
            s = s.replace('{' + key + '}',self.params[key])
        #返回替换后参数的值
        return s

    def assertequals(self,key,value):
        '''
        断言json的结果里面，某个键的值和value相等
        :param key:json结果中的键
        :param value:预期的值
        :return:无
        '''
        value = self.__get_param(value)
        res = str(self.result)
        # logger.info(self.jsons)
        try:
            # print(self.jsons)
            if key not in self.jsons:
                pass
            else:
                res = str(jsonpath.jsonpath(self.jsons,str(key))[0])
        except Exception as e:
            logger.info('没有对应的' + key)
            logger.exception(e)

        if res == str(value):
            logger.info('PASS')
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, str(self.jsons))
        else:
            logger.info('FAIL')
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(self.jsons))






