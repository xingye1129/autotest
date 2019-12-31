from common.Excel import Read
from common import logger

class Res:
    """
    统计Excel用例执行结果信息
    """

    def __init__(self):
        # 用于记录所有模块分组信息名称
        self.sumarry = {}

    def get_res(self,result_path):

        self.sumarry.clear()
        status = "Fail"
        #标识是否有失败
        flag = True
        #统计用例的总条数
        totalcount = 0
        #统计所有用例中通过用例的条数
        totalpass = 0

        read = Read()
        read.open_excel(result_path)
        #读取第一行的数据
        read.readline()
        #读取第二行的数据
        line = read.readline()
        self.sumarry['runtype'] = line[1]
        self.sumarry['title'] = line[2]
        self.sumarry['starttime'] = line[3]
        self.sumarry['endtime'] = line[4]
        #获取所有的sheet页面：
        for sheetnames in read.get_sheets():
            # logger.info(sheetnames)
            #从第一个页面开始解析
            read.set_sheets(sheetnames)
            #获取所有sheet页的行数row，用来遍历
            row = read.rows
            #设置从第二行开始读取
            read.r = 1

            #遍历sheet里面的所有用例
            for i in range(1,row):
                line = read.readline()
                # logger.info(line)
                # 查找记录了分组信息的行
                # 如果第一列（分组信息）和第二列（类别或用例名）同时为空,则是用例，执行非用例的操作
                #反之不同时为空，则不是用例
                if not (line[0] == '' and line[1] == ''):
                    pass
                # 第一列信息和第二列信息均为空的行，即用例行，这时开始进行用例数、通过数、状态的统计。
                else:
                    # 判断执行结果列，如果为空，将flag置为false,视为该行有误，不纳入用例数量计算
                    if len(line) < 7 or line[7] == '':
                        flag = False
                    # 执行结果不为空，则将用例统计数自增
                    else:
                        totalcount = totalcount + 1
                        # logger.info(totalcount)
                        if line[7] == 'PASS':
                            totalpass+= 1
                        else:
                            # 出现了用例执行结果不是PASS的情况，则视为当前分组执行失败。

                            flag = False
             #for循环结束
         #所有用例的执行情况
        # logger.info(totalpass)
        #如果flag为真，也就是所有为PASS,则测试状态为pass
        if flag:
            status = "PASS"
        else:
            status = "Fail"
        try:
            p = int(totalpass * 10000 / totalcount)
            passrate = str(p/100) +'%'
            # logger.info(passrate)
        except Exception as e:
            p = 0.0
            logger.exception(e)
        # 用例总数
        self.sumarry["casecount"] = str(totalcount)
        self.sumarry["passrate"] = str(passrate)
        self.sumarry['status'] = status
        # logger.info(self.sumarry)
        return  self.sumarry




if __name__=='__main__':
    res =Res()
    R =res.get_res('../lib/results/result-HTTP接口用例.xls')
    print(R)


