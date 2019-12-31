# -*- coding: UTF-8 -*-

from common.Excel import *
from common import logger,config
from common.Mail import Mail
from common.Excel import Read
from common.mysql import Mysql
from AutoHttp.withHttp import *
from common.excelresult import Res
from Web.WithWeb import Webinter
from APP.Withapp import APP
import inspect
import datetime


"""
    这是整个自动化框架的主代码运行入口
    powered by xingye
    at: 2019/11/19
"""
def runcase(line,http):
    #分组信息不用执行'
    if len(line[0]) > 0 or len(line[1]) > 0:
        return
    #反射获取关键字函数
    func = getattr(http,line[3])
    #获取关键字列表
    agrs = inspect.getfullargspec(func).__str__()
    agrs = agrs[agrs.find('args=') + 5:agrs.rfind(', varargs=None')]
    agrs = eval(agrs)
    agrs.remove('self')
    # 不接收参数的调用
    if len(agrs) == 0:
        func()
    #接收一个参数
    if len(agrs) == 1:
        func(line[4])
        return
    # 接收二个参数
    if len(agrs) == 2:
        func(line[4],line[5])
        return
    #接收三个参数
    if len(agrs) ==3:
        func(line[4],line[5],line[6])

if __name__=='__main__':
    read =Read()
    xslname = 'SOAP'
    read.open_excel('./lib/cases/'+xslname +'.xls')
    sheetname = read.get_sheets()

    config.get_config('./conf/conf.properties')
    mysql = Mysql()
    mysql.init_mysql('./conf/userinfo.sql')

    writer = Writer()
    writer.cope_open('./lib/cases/'+xslname +'.xls', './lib/results/result-'+xslname +'.xls')

    writer.set_sheet(sheetname[0])
    writer.write(1, 3, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    read.readline()
    http = None
    casetype = read.readline()[1]
    if casetype == 'HTTP':
        http = HTTP(writer)
    if casetype == 'SOAP':
        http = SOAP(writer)
    if casetype == 'WEB':
        http = Webinter(writer)
    if casetype == 'APP':
        http = APP(writer)



    for sheet in sheetname:
        #设置当前读取的sheet页
        read.set_sheets(sheet)
        #保持读写在同一个sheet页
        writer.set_sheet(sheet)
        for i in range(read.rows):
            writer.row = i
            line = read.readline()
            runcase(line,http)
    writer.set_sheet(sheetname[0])
    writer.write(1, 4, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    writer.save_close()

    #读取解析结果
    res =Res()
    result = res.get_res('./lib/results/result-'+xslname +'.xls')
    logger.info(result)
    config.get_config('./conf/conf.properties')
    logger.info(config.config)
    #替换html模板中的数据
    html = str(config.config['mailtxt'])
    html = html.replace('status',result['status'])
    if result['status'] == 'Fail':
        html = html.replace('#00d800','red')
    html = html.replace('title', result['title'])
    html = html.replace('runtype',result['runtype'])
    html = html.replace('passrate',result['passrate'])
    html = html.replace('starttime',result['starttime'])
    html = html.replace('casecount',result['casecount'])
    html = html.replace('endtime',result['endtime'])
    mail = Mail()
    # mail.mail_info['filepaths'] = html
    # mail.mail_info['filenames'] ='测试报告附件'
    mail.send(html)
