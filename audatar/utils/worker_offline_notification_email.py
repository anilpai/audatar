import time
from utils.mail import HomeAwayMailer
from audatar import audatar_config
import sys


class WorkerOfflineNotificationEmail:
    def __init__(self):
        self.mailer = HomeAwayMailer()

    def send_WorkerOfflinemail_as_html(self):

        html = """<html>
            <head>
            <style>
            table {border-collapse: collapse;}
            table, th, td {border: 1px solid black; padding: 5px;}
            th {background-color: #ADD8E6;}
            h1 {color: blue;}
            </style>
            </head>
            <body>
            <h1>ACTION REQUIRED</h1>"""

        fromAddr = 'audatar@homeaway.com'
        toAddr = 'analyticsengineeringoperations@groups.homeawaycorp.com'

        current_time = time.ctime()
        env = audatar_config.env.capitalize()

        html += """ <h3>Error Message: Audatar Worker just went Offline !!!</h3>"""
        html += '</body></html>'
        self.mailer.sendhtml('Could not check {0} Audatar Worker at {1}!!!'.format(
            env, current_time), html, fromAddr, toAddr)
        sys.exit('Error Message: Audatar Worker is Offline')
