#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email import Utils

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import os
import commands
import sys
import logging
import datetime
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

mail_log_path = "/var/log/zabbix/send_alert_mail.log"
sms_log_path = "/var/log/zabbix/send_alert_sms.log"
wechat_log_path = "/var/log/zabbix/send_alert_wechat.log"
abort_log_path = "/var/log/zabbix/send_alert_abort.log"
max_mail_count = 20
max_sms_count = 25
max_wechat_count = 30


def is_out_one_minute(filename, count, content):
    if os.path.exists(filename):
        try:
            curr_lines = commands.getoutput("/bin/wc -l " + filename + " | awk '{print $1}'").strip()
            if int(curr_lines) > count:
                c_time = commands.getoutput("/bin/tail -n " + str(count) + " " + \
                                  filename + " | head -1 | awk '{print $2,$3}'").strip()

                if c_time:
                    c_time = datetime.datetime.strptime(c_time, '%Y-%m-%d %H:%M:%S.%f')
                    cost = (datetime.datetime.now() - c_time).seconds
                    if cost < 30:
                        log_write(abort_log_path, False,
                                  'Abort %s,c_time is %s' % (content, c_time))
                        os._exit(1)
        except Exception, e:
            log_write(abort_log_path, False,
                      'Abort %s,exception is %s' % (content, str(e)))
            os._exit(1)


def send_mail(send_to, subject, content):
    mail_user = "ops_notice@shixh.com"
    #mail_password = "JKFaQZYyUbS93gVCwVbT"
    mail_password = "JKFaQZYyUbS93gVC"
    # mail_host = "smtp.exmail.qq.com"
    # mail_host = "smtp.ym.163.com"
    mail_host = "smtp.mxhichina.com"
    state = ''
    msg = ''

    subject = subject.decode('utf-8')
    content = content.decode('utf-8')

    message = MIMEText(content, _subtype='plain', _charset='utf-8')
    message['Subject'] = subject
    message['From'] = u'系统监控<' + mail_user + ">"
    message['To'] = send_to
    message['Date'] = Utils.formatdate(localtime=1)
    message['Message-ID'] = Utils.make_msgid()
    message = message.as_string()

    try:
     #   s = smtplib.SMTP_SSL(mail_host, 465)
     #   s = smtplib.SMTP_SSL(mail_host, 994)
        s = smtplib.SMTP_SSL(mail_host, 465)
        s.login(mail_user, mail_password)
        is_out_one_minute(mail_log_path, max_mail_count, send_to + " " + subject)
        s.sendmail(mail_user, send_to, message)
        s.close()
        state = True
        msg = "MAIL TO %s,subject is %s" % (send_to, subject)
    except Exception, e:
        state = False
        msg = "MAIL TO %s,error is %s" % (send_to, str(e))
    finally:
        return state, msg


def send_sms(mobile, content):
    sms_api = "http://sms.shixh.tp/manage/sms/sendBatchSms"
    headers = {'content-type': 'application/json', 'user-agent': 'zabbix'}
    post_data = {
                    "param": {
                        "appCode": "zabbix",
                        "data": [
                            {
                                "content": content,
                                "mobile": mobile,
                                "sign":"sxh"
                            }
                        ]
                    }
                }
    state = ''
    msg = ''

    try:
        is_out_one_minute(sms_log_path, max_sms_count, mobile + " " + content)
        req = requests.post(sms_api, data=json.dumps(post_data), verify=False, headers=headers)
        response = req.json()

        if response["success"]:
            state = True
            msg = "SMS TO %s,content is %s" % (mobile, content)
        else:
            state = False
            msg = "SMS TO %s,content is %s" % (mobile, response["message"])
    except Exception, e:
        state = False
        msg = "SMS TO %s,error is %s" % (mobile, str(e))
    finally:
        return state, msg

def send_wechat(userOpenId,subject,content):
    appID = "wxb7fefb5525efa70c"
    appsecret = "618a9cf5845fe7ff9da39bd983c40ed6"
    tempId = "l25sCa4tmOogIArne9IeouB7p_K63wmI0qavttOQrRs"
    tempIdReconvery = "3hSQtYkmxn0sCZlI7nrvwklCAH3TblX_V3CKCl4CFm0"
    sendMessageUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token="
    template = {'touser': "",
                'template_id': "",
                'url ': "",
                'topcolor ': '#7B68EE',
                'data': ""}
    tonkenURL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=" + appID + "&secret=" + appsecret
    res = requests.post(tonkenURL)
    token = json.loads(res.text)["access_token"]
    state = ''
    msg = ''

    try:
        is_out_one_minute(wechat_log_path, max_wechat_count, userOpenId + " " + subject)
        template["touser"] = userOpenId
        template["url"] = "https://zabbix.shixh.com/zabbix"

        if "恢复" in subject:
            template["template_id"] = tempIdReconvery
            template["data"]  = {"first": {"value": subject, "color": "#173177"},
                                    "keyword3": {"value": content, "color": "#173177"},
                                    "keyword1": {"value": "OK", "color": "#173177"},
                                    "keyword2": {"value": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "color": "#173177"},
                                    "remark": {"value": "更多内容请登录https://zabbix.shixh.com/zabbix查看！", "color": "#173177"}}
            res = requests.post(sendMessageUrl + token, json.dumps(template))
            state = True
            msg = "WECHAT TO %s,subject is %s" % (userOpenId, subject)
            return res
        else:
            template["template_id"] = tempId
            template["data"] = {"first": {"value": subject, "color": "#173177"},
                    "keyword2": {"value": content, "color": "#173177"},
                    "keyword1": {"value": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "color": "#173177"},
                    "remark": {"value": "更多内容请登录https://zabbix.shixh.com/zabbix查看！", "color": "#173177"}}
            res = requests.post(sendMessageUrl + token, json.dumps(template))
            state = True
            msg = "WECHAT TO %s,subject is %s" % (userOpenId, subject)
            return res
    except Exception, e:
        state = False
        msg = "WECHAT TO %s,error is %s" % (userOpenId, str(e))
    finally:
        return state, msg


def log_write(path, stats, msg):
    t = datetime.datetime.now()
    logging.basicConfig(filename=path,
                        level=logging.DEBUG,
                        format='%(levelname)s %(message)s')

    if stats:
        logging.info(str(t) + " " + msg)
    else:
        logging.error(str(t) + " " + msg)


if __name__ == "__main__":
    if sys.argv[1] == 'mail':
        send_to = sys.argv[2]
        subject = sys.argv[3]
        content = sys.argv[4]
        stats, msg = send_mail(send_to, subject, content)
        log_write(mail_log_path, stats, msg)
    elif sys.argv[1] == 'sms':
        mobile = sys.argv[2]
        subject = sys.argv[3]
        stats, msg = send_sms(mobile, subject)
        log_write(sms_log_path, stats, msg)
    elif sys.argv[1] == 'wechat':
         userOpenId = sys.argv[2]
         subject = sys.argv[3]
         content = sys.argv[4]
         stats, msg = send_wechat(userOpenId, subject, content)
         log_write(wechat_log_path, stats, msg)
    if not stats:
        print msg
        sys.exit(1)
