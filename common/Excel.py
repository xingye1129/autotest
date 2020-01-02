#coding:utf8
import os
import xlwt,xlrd
from xlutils.copy import copy


class Read:
    """
        用来读取Excel文件中的内容
    """

    def __init__(self):
        #整个exce工作簿缓存
        self.workbook = None
        #当前的sheet页
        self.sheet = None
        #当前sheet的行数
        self.rows = 0
        #当前读到的行数
        self.r = 0

    def open_excel(self,srcfile):
        #如果要打开的文件不存在，就报错
        if not os.path.isfile(srcfile):
            print("error：%s not exist!" % (srcfile))
            return
        #设置要读取的excel使用utf8编码
        xlrd.Book.encoding = "utf8"
        #读取excel内容到缓存workbook
        self.workbook = xlrd.open_workbook(filename=srcfile)
        #选取第一个sheet页面
        self.sheet = self.workbook.sheet_by_index(0)
        #设置rows为当前sheet页面的行数
        self.rows = self.sheet.nrows
        #打印当前sheet页的行数
        # print(self.rows)
        #设置默认读取为第一行
        self.r = 0
        return



    #获取sheet页面
    def get_sheets(self):
        #获取所有的sheet页的名字，返回一个列表
        sheets = self.workbook.sheet_names()
        # print(sheets)
        return sheets

    #切换sheet页面
    def set_sheets(self,name):
        #通过sheet页的名字，切换到sheet页面
        self.sheet = self.workbook.sheet_by_name(name)
        #获取当前sheet页面的所有行
        self.rows = self.sheet.nrows
        # print(self.rows)
        self.r = 0
        return

    #逐行读取
    def readline(self):
        #定义row1变量，用来返回没一行中每一列的值
        row1 = None

        #如果还没有到最后一行，则往下读取一行
        if self.r < self.rows:
            #读取每r行的内容，并返回一个列表赋值给row，其中self.r指的是每一行
            row = self.sheet.row_values(self.r)
            #设置下一次读取r的下一行
            # self.r = self.r + 1
            self.r += 1
            #辅助循环里面的列
            i = 0
            row1 = row
            #读取的数据变为字符串，从列表中遍历
            for strs in row:
                row1[i] = str(strs)
                i +=1
        # print(row1)
        return row1


class Writer:
    """
        用来复制写入的Excel文件，保存在新的文件夹中
    """
    def __init__(self):
        #读取需要复制的Excel文件，保存在workbook缓存中
        self.workbook = None
        #拷贝的工作空间
        self.wb = None
        #当前工作的sheet页
        self.sheet = None
        #记录生成的文件，用来保存
        self.df = None
        #记录的写入的行
        self.row = 0
        #记录写入的列
        self.clo = 0



    #复制并打开excel
    def cope_open(self,srcfile,dstfile):
        #判断要复制的文件是否存在
        if not os.path.isfile(srcfile):
            print("erro:" + srcfile + '\t' + "not exist!")
            return

        #判断新建的文件是否存在，如果存在，则提示
        if os.path.isfile(dstfile):
            print("warning: " + dstfile + "file is exist")

        #记录要保存的文件
        self.df = dstfile
        #读取到excel缓存
        #formatting_info带原有文件格式的辅助
        self.workbook = xlrd.open_workbook(filename=srcfile, formatting_info=True,)
        #拷贝
        self.wb = copy(self.workbook)
        #默认使用第一个sheet
        # sheet = self.wb.get_sheet('授权接口')
        # print(sheet)
        return

    #获取sheet页面
    def get_sheets(self):
        #获取所有sheet的名字,并返回一个列表
        sheets = self.workbook.sheet_names()
        # print(sheets)
        return sheets

    #切换sheet页
    def set_sheet(self,name):
        #通过sheet名字，切换到sheet页面
        self.sheet = self.wb.get_sheet(name)
        #打印出选择sheet页的缓存对象
        # print(self.sheet)
        return

    def write(self, r, c,value):
        #获取要写入的单元格
        def _getCell(sheet, r, c):
            """ HACK: Extract the internal xlwt cell representation. """
            #获取行
            row = sheet._Worksheet__rows.get(r)
            if not row:
                return None
            #根据选择的行来获取单元格
            clo = row._Row__cells.get(c)
            return clo

        #获取要写入的单元格
        cell = _getCell(self.sheet, r, c)
        #写入值
        self.sheet.write(r, c, value)

        if cell:
            ncell = _getCell(self.sheet, r, c)
            if ncell:
                #设置写入后格式和写入前一样
                ncell.xf_idx = cell.xf_idx

        return

    #保存
    def save_close(self):
        #保存复制后的到目标文件中，-》到硬盘
        self.wb.save(self.df)
        return












#调试代码

if __name__=='__main__':
    read =Read()
    read.open_excel('../lib/cases/HTTP接口用例.xls')
    sheetname = read.get_sheets()
    for sheet in sheetname:
        read.set_sheets(sheet)
        for i in range(read.rows):
            print(read.readline())

    # writer = Writer()
    # writer.cope_open('../lib/cases/HTTP接口用例.xls', '../lib/results/result-HTTP接口用例.xls')
    # sheetname = writer.get_sheets()
    # writer.set_sheet(sheetname[0])
    # writer.write(1, 1, 'HTTP')
    # writer.save_close()