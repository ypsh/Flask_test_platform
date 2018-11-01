# -*- coding: UTF-8 -*-
import configparser
import logging
import smtplib
import socket
from email.mime.text import MIMEText

from com.common.aesUtil import AesUtil
from com.common.getPath import Path


class SentMail:
    def __init__(self):
        self.mail_host = 'smtp.163.com'
        self.mail_user = 'ypshwork@163.com'
        self.mail_password = 'xyd218cd2ece742d22d6e41759c12ea60121081029'
        self.port = 465
        self.sender = 'ypshwork@163.com'
        self.global_path = Path().get_current_path()
        conf = configparser.ConfigParser()
        conf.read(self.global_path + '/config/config.ini')
        self.receivers = eval(conf.get('mail', 'resport_reciver'))

    def send(self, to_receiver, subject, body):
        # 设置邮件正文，这里是支持HTML的
        msg = MIMEText(body, 'html')
        # 设置正文为符合邮件格式的HTML内容
        msg['subject'] = subject
        # 设置邮件标题
        msg['from'] = self.sender
        # 设置发送人
        msg['to'] = ",".join(to_receiver)
        try:
            send = smtplib.SMTP_SSL(self.mail_host, self.port)
            # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
            send.login(self.mail_user, AesUtil().decypt(self.mail_password))
            # 登陆邮箱
            send.sendmail(self.sender, self.receivers, msg.as_string())
            # 发送邮件！
            logging.info('Done.sent email success')
        except smtplib.SMTPException as e:
            logging.error('Error.sent email fail' + str(e))

    def snd_report(self, args):
        body = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>测试报告</title>
</head>
<body>
<h1>自动化执行结果通知</h1>
<p>批次号：%s</p>
<p>总计：%s 条</p>
<p>通过：%s 条</p>
<p>失败：%s 条</p>
<p>详细结果请见：</p>
<a href="%s" target="_blank" name="dttl">
%s</a>
<p>请使用批次号到系统中查看报告详情</p>
</body>
</html>
        '''

        try:
            if args['data'] != '' and args['data']['FAIL'] != 0:
                body = body % (args['data']['batch_number'],
                               str(args['data']['Total']),
                               str(args['data']['PASS']),
                               str(args['data']['FAIL']),
                               'http://' + str(self.get_host_ip()) + ':5000/autotest/testreport',
                               'http://' + str(self.get_host_ip()) + ':5000/autotest/testreport')
                # subject = u'【自动化】' + str(result['data']['batch_number']) + '执行结果通知,有失败用例请关注！！！'
                subject = str(args['data']['batch_number']) + '执行结果通知,有失败用例请关注！！！'
                self.send(to_receiver=self.receivers, subject=subject, body=body)
        except Exception as e:
            logging.error('邮件发送失败' + str(e))

    def get_host_ip(self):
        """
        查询本机ip地址
        :return: ip
        """
        global s
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip


if __name__ == '__main__':
    result = {'message': True,
              'data': {'batch_number': 12312314123, 'Total': 100,
                       'FAIL': 30, 'PASS': 70}}
    SentMail().snd_report(result)
