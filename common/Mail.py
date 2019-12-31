from common import logger,config
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    """
    用来获取配置并发送邮件
    """

    def __init__(self):

        self.mail_info = {}
        #发件人
        self.mail_info['from'] = config.config['mail']
        self.mail_info['username'] = config.config['mail']
        #smtp服务器域名
        self.mail_info['hostname'] = 'smtp.' + config.config['mail'][
                        config.config['mail'].rfind('@') + 1:config.config['mail'].__len__()]
        #发件人的密码
        self.mail_info['password'] = config.config['pwd']
        #发件人
        self.mail_info['to'] = str(config.config['mailto']).split(',')
        #抄送人
        self.mail_info['cc'] = str(config.config['mailcopy']).split(',')
        #邮件标题
        self.mail_info['mail_subject'] = config.config['mailtitle']
        self.mail_info['mail_encoding'] = config.config['mail_encoding']
        #附件内容
        self.mail_info['filepaths'] = []
        self.mail_info['filenames'] = []

    def send(self,text):
        # 这里使用SMTP_SSL就是默认使用465端口，如果发送失败，可以使用587
        smtp = SMTP_SSL(self.mail_info['hostname'])
        smtp.set_debuglevel(0)

        ''' SMTP 'ehlo' command.
                Hostname to send for this command defaults to the FQDN of the local
                host.
        '''

        smtp.ehlo(self.mail_info['hostname'])
        smtp.login(self.mail_info['username'], self.mail_info['password'])

        #普通的HTML邮件
        # msg = MIMEText(text, 'html', self.mail_info['mail_encoding'])

        #带附件的发送
        msg = MIMEMultipart()
        msg.attach(MIMEText(text, 'html',self.mail_info['mail_encoding']))
        msg['Subject'] = Header(self.mail_info['mail_subject'], self.mail_info['mail_encoding'])
        msg['from'] = self.mail_info['from']

        logger.debug(self.mail_info)
        logger.debug(text)
        msg['to'] = ','.join(self.mail_info['to'])
        msg['cc'] = ','.join(self.mail_info['cc'])
        receive = self.mail_info['to']
        receive += self.mail_info['cc']
        # 添加附件
        for i in range(len(self.mail_info['filepaths'])):
            att1 = MIMEText(open(self.mail_info['filepaths'][i], 'rb').read(), 'base64', 'utf-8')
            att1['Content-Type'] = 'application/octet-stream'
            att1['Content-Disposition'] = 'attachment; filename= "' + self.mail_info['filenames'][i] + '"'
            msg.attach(att1)

        try:
            smtp.sendmail(self.mail_info['from'], receive, msg.as_string())
            smtp.quit()
            logger.info('邮件发送成功')
        except Exception as e:
            logger.error('邮件发送失败：')
            logger.exception(e)

#调试
if __name__ == '__main__':
    config.get_config('../conf/conf.properties')
    # logger.debug(config.config)
    # logger.debug(config.config)
    mail = Mail()
    mail.mail_info['filepaths'] = ['E:\\Software\\module.html']
    mail.mail_info['filenames'] = ['Xytest.html']
    html = config.config['mailtxt']
    mail.send(html)