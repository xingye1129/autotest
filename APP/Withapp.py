# -*- coding: UTF-8 -*-
from appium import webdriver
import traceback,time,os,threading
from common.logger import logger

class APP:
    """
            这是APP自动化的关键字库
            powered by xingye
            at: 2019/12/16
    """

    def __init__(self,writer):
        self.driver = None
        self.ele = None
        self.t = 20
        self.writer = writer

    def runappium(self, path='', port='', t=''):
        """
        启动appium服务
        :path：appium的安装路径
        :param port: 服务的启动端口
        :t：等待时间
        :return:
        """
        try:
            if path == '':
                cmd = 'node C:\\Users\\Xy\\AppData\\Local\\Programs\\Appium\\resources\\app\\node_modules\\appium\\build\\lib\\main.js'
            else:
                cmd = 'node ' + path + '\\resources\\app\\node_modules\\appium\\build\\lib\\main.js'
            if port == '':
                cmd += ' -p 4723'
            else:
                self.port = port
                cmd += ' -p ' + port
                print(cmd)
            if t == '':
                t = 5
            else:
                t = int(t)

            # 启动appium服务
            def run(cmd):
                try:
                    os.popen(cmd).read()
                except Exception as e:
                    pass

            th = threading.Thread(target=run, args=(cmd,))
            th.start()
            time.sleep(t)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))



    def runapp(self,conf,t='20'):
        """
        连接appium服务器，并根据conf配置，启动待测试APP
        :param conf:APP的启动配置，为标准json字符串
        :param t:
        :return:
        """
        try:
            t = int(t)
            self.t = t
            conf = eval(conf)
            self.driver = webdriver.Remote('http://127.0.0.1:4728/wd/hub', conf)
            self.driver.implicitly_wait(t)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def __findele(self,xpath):
        """
        定位元素
        :param xpath:元素的定位路径，支持accessibility_id，id，xpath
        :return:找到的元素，如没找到，就返回None
        """
        try:
            if xpath.startswith('//'):
                self.ele = self.driver.find_element_by_xpath(xpath)
            else:
                try:
                    self.ele = self.driver.find_element_by_accessibility_id(xpath)
                except Exception as e:
                    self.ele = self.driver.find_element_by_id(xpath)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

        return self.ele




    def input(self,xpath,content):
        ele = self.__findele(xpath)
        if ele is None:
            logger.error('NO such element ' + xpath)
        else:
            try:
                ele.clear()
                ele.send_keys(content)
                self.writer.write(self.writer.row, 7, 'PASS')
            except Exception as e:
                self.writer.write(self.writer.row, 7, 'FAIL')
                self.writer.write(self.writer.row, 8, str(traceback.format_exc()))



    def click(self,xpath):

        ele = self.__findele(xpath)
        if ele is None:
            logger.error('NO such element '+ xpath)
        else:
            try:
                ele.click()
                self.writer.write(self.writer.row, 7, 'PASS')
            except Exception as e:
                self.writer.write(self.writer.row, 7, 'FAIL')
                self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def quit(self):
        try:
            self.driver.quit()
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))
    def implicitly_waits(self,t):
        self.driver.implicitly_wait(t)

    def time(self,t):
        time.sleep(int(t))
