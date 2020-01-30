---
layout: post
title:  python发送邮件
category: 技术
tags:  
    - python
    - smtp
    - email
keywords: 
description: 
---

# python发送邮件

提供一个 python 发送邮件的示例，该示例包括：
- 同时发送给多个用户
- 以附件形式发送多个excel文件

```
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from typing import NamedTuple


class SourceEmailInfo(NamedTuple):
    """ email info """
    email_address: str
    email_password: str
    smtp_host: str
    smtp_port: int


def send_email(source_email_info: SourceEmailInfo, to_email_list: [str], title: str, content: str, file_name_list: [str] = None, ):
    msg = MIMEMultipart()

    # 基本信息
    msg['From'] = source_email_info.email_address
    msg['To'] = ",".join(to_email_list)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = title

    # 邮件正文
    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    # 添加附件
    if file_name_list:
        # todo: gbk, only for excel file
        for file_name in file_name_list:
            excel_file_obj = MIMEApplication(open(file_name, 'rb').read())
            excel_file_obj.add_header('Content-Disposition', 'attachment', filename=('gbk', '', os.path.basename(file_name)))
            msg.attach(excel_file_obj)

    # 发邮件
    smtp_obj = smtplib.SMTP_SSL(source_email_info.smtp_host, source_email_info.smtp_port)
    smtp_obj.login(source_email_info.email_address, source_email_info.email_password)
    smtp_obj.sendmail(source_email_info.email_address, to_email_list, msg.as_string())
    smtp_obj.quit()


```

完整的源码见[email_utils.py](https://github.com/frkhit/pyxtools/blob/master/pyxtools/basic_tools/email_utils.py)