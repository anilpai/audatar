import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from audatar import audatar_config


class HomeAwayMailer:

    def __init__(self):
        self.smtpServer = audatar_config.mail_server
        self.smtpObj = smtplib.SMTP(self.smtpServer)

    def _to(self, toAddr, ccAddr):
        to = []
        if type(toAddr) is list:
            to.extend(toAddr)
        elif toAddr is not None:
            to.append(toAddr)
        if type(ccAddr) is list:
            to.extend(ccAddr)
        elif ccAddr is not None:
            to.append(ccAddr)
        return to

    def _createmessage(self, subject, body, fromAddr, toAddr, ccAddr, mimetype):
        message = MIMEMultipart('altnernative')
        message['Subject'] = subject
        if type(toAddr) is list and len(toAddr) > 1:
            message['To'] = ','.join(toAddr)
        elif type(toAddr) is list and len(toAddr) == 1:
            message['To'] = toAddr[0]
        elif type(toAddr) is not list:
            message['To'] = toAddr
        message['From'] = fromAddr
        if ccAddr is not None and type(ccAddr) is list and len(ccAddr) > 1:
            message['CC'] = ','.join(ccAddr)
        elif ccAddr is not None and type(ccAddr) is list and len(ccAddr) == 1:
            message['CC'] = ccAddr[0]
        elif ccAddr is not None and type(ccAddr) is not list:
            message['CC'] = ccAddr

        part1 = None
        if (mimetype == 'html'):
            part1 = MIMEText(body.encode('utf-8'), 'html', 'utf-8')
        else:
            part1 = MIMEText(body, 'plain')

        message.attach(part1)
        return message

    def sendtext(self, subject, body, fromAddr, toAddr, ccAddr=None):
        message = self._createmessage(subject, body, fromAddr, toAddr, ccAddr, 'plain')
        self.smtpObj.sendmail(fromAddr, self._to(toAddr, ccAddr), message.as_string())

    def sendhtml(self, subject, body, fromAddr, toAddr, ccAddr=None):
        message = self._createmessage(subject, body, fromAddr, toAddr, ccAddr, 'html')
        self.smtpObj.sendmail(fromAddr, self._to(toAddr, ccAddr), message.as_string())
