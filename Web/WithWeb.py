from selenium import webdriver
import os
import time,traceback
from common.logger import logger
from selenium.webdriver.common.action_chains import ActionChains
class  Webinter:

    def __init__(self,writer):
        self.driver = None
        self.title = ''
        self.current = None
        self.all_handler = None
        self.writer = writer
        self.text = ''

    def Openbrower(self,type = 'Chrome'):
        if type == 'Chrome' or type == '':
            # 创建一个ChromeOptions对象
            option = webdriver.ChromeOptions()
            # 去掉浏览器提示条的提示
            option.add_argument('disbale-infobars')

            try:
                # 异常处理，如果获取到，使用获取到的路径
                userdir = os.environ['USERPROFILE']
                logger.info(userdir)
            except Exception as e:
                userdir = 'C:\\Users\\Xy'
                # 如果没有获取到，则使用默认的文件路径
                logger.exception(e)
            userdir += '\\AppData\\Local\\Google\\Chrome\\User Data'
            userdir = '--user-data-dir=' + userdir
            # 添加用户目录
            option.add_argument(userdir)
            #调用浏览器
            self.driver = webdriver.Chrome(executable_path="./Web/lib/chromedriver.exe",chrome_options=option)
            self.driver.implicitly_wait(3)
            # self.driver.find_element_by_xpath().text
        if type == 'Ie':
            self.driver = webdriver.Ie(executable_path='./Web/lib/IEDriverServer.exe',desired_capabilities=None)
        if type == 'gc':
            self.driver = webdriver.Firefox(executable_path="./Web/lib/geckodriver.exe")

    def get(self,url):
        """
        打开URL页面
        :param url:url地址
        :return: 无
        """
        try:
            self.driver.get(url)
            self.writer.write(self.writer.row, 7, 'PASS')
            self.writer.write(self.writer.row, 8, url)
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))
    def click(self,xpath):
        """
        点击元素
        :param xpath:要点击元素的xpath定位
        :return: 无
        """
        try:
            re = self.driver.find_element_by_xpath(xpath)
            re.click()
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def input(self,xpath,content):
        """
        通过定位输入内容
        :param xpath: 输入框的xpath路径
        :param content: 要输入的内容
        :return: 无
        """
        try:
            self.driver.find_element_by_xpath(xpath).clear()
            self.driver.find_element_by_xpath(xpath).send_keys(content)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def intoiframe(self,xpath):
        """
        进入iframe框
        :param xpath:iframe所在的xpath路径
        :return: 无
        """
        try:
            self.driver.switch_to_frame(self.driver.find_element_by_xpath(xpath))
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def outiframe(self):
        """
        退出iframe页面，返回到根目录
        :return: 无
        """
        try:
            self.driver.switch_to_default_content()
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def Moveto(self,xpath):
        '''
        滑动窗口到目标元素，实现翻页
        :param xpath: 目标元素的xpath路径
        :return: 无
        '''
        try:
            actions = ActionChains(self.driver)
            ele = self.driver.find_element_by_xpath(xpath)
            actions.move_to_element(ele).perform()
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def excutejsLeft(self,y):
        '''
        横行滑动滚轴
        :param y: 向右滑动的坐标长度
        :return: 无
        '''
        try:
            js = "document.documentElement.scrollLeft=" + str(y)
            self.driver.execute_script(js)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def assertequals(self,p,value):
        try:
            p = p.replace('{text}',self.text)
            if str(p) == str(value):
                self.writer.write(self.writer.row, 7, 'PASS')
            else:
                self.writer.write(self.writer.row, 7, 'FAIL')
                self.writer.write(self.writer.row, 8, str(p))
        except Exception as e:
            self.writer.write(self.writer.row, 7, 'FAIL')
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def excutejs(self,y):
        '''
        通过javascript实现向下滑动滚轴
        :param y: 向下滑动的坐标长度
        :return: 无
        '''
        try:
            js = "var q=document.documentElement.scrollTop=" + str(y)
            self.driver.execute_script(js)
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, logger.exception(e))


    def windowsHandler(self):
        '''
        切换窗口，并关闭当前的窗口
        :return:无
        '''
        self.current = self.driver.current_window_handle
        print(self.current)
        self.all_handler = self.driver.window_handles
        print(self.all_handler)
        try:
            if len(self.all_handler)>1 and self.current == self.all_handler[0]:
                self.driver.close()
                self.current = self.all_handler[1]
                self.driver.switch_to_window(self.current)
                self.writer.write(self.writer.row, 7, 'PASS')
            else:
                pass
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def gettitle(self):
        '''
        获取当前窗口标题
        :return: 返回当前窗口标题
        '''
        try:
            self.title =self.driver.title
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def implicitly_wait(self,outtimes):
        '''
        隐式等待
        :param outtimes: 最长等待的时间
        :return: 无
        '''
        try:
            self.driver.implicitly_wait(outtimes)
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, logger.exception(e))

    def sleep(self,s):
        try:
            time.sleep(int(s))
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))

    def gettext(self,xpath):
        try:
            self.text = self.driver.find_element_by_xpath(xpath).text
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


    def quit(self):
        try:
            self.driver.quit()
            self.writer.write(self.writer.row, 7, 'PASS')
        except Exception as e:
            logger.exception(e)
            self.writer.write(self.writer.row, 8, str(traceback.format_exc()))


if __name__=='__main__':
    driver = Webinter()
    driver.Openbrower()
    driver.quit()