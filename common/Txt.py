from common import logger

class Txt:
    """
    用来读写文件
    """

    #构造函数打开txt
    def __init__(self,path, mode='r',coding='utf8'):

        self.data = []
        self.f = None
        if mode =='r':
            #逐行读取,并存在列表中
            for line in open(path, encoding=coding):
                self.data.append(line)
            #去掉末尾的换行
            for i in range(self.data.__len__()):
                #处理非法字符串
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
                #去掉末尾的缓行
                self.data[i] = self.data[i].replace('\n','')
            return

        if mode == 'w':
            #打开可读文件，mode=a代表在末尾追加
            self.f = open(path,'a',encoding=coding)
            return
        if mode == 'rw':
            for line in open(path,encoding=coding):
                self.data.append(line)
            #去掉换行
            for i in range(self.data.__len__()):
                #处理特殊字符
                self.data[i] = self.data[i].encode('utf-8').decode('utf-8-sig')
                self.data[i] = self.data[i].replace('\n','')

            self.f = open(path,'a',encoding=coding)
            return

    #读取
    def read(self):
        """
        将txt文件格式按行读取，并储存未列表
        :return:返回txt所有内容的列表
        """
        return self.data

    #写入
    def writeline(self,s):
        """
        往txt文件末尾写入一行
        :param s:需要写入的内容，如果需要换行自己添加\n
        :return:无
        """
        if self.f is None:
            logger.error("未打开可写入txt文件")
        self.f.write(str(s))

    #保存
    def save_close(self):
        """
        写入文件后，必须要保存
        :return:无
        """
        if self.f is None:
            logger.error("未打开可写入txt文件")
        self.f.close()



#调试
if __name__=='__main__':
    reader = Txt('../conf/conf.properties',mode='r')
    t = reader.read()
    print(t)

    write = Txt('../lib/logs/all.log',mode='w')
    write.writeline('写入成功')
    write.save_close()

