# -*-coding:utf-8-*- 
# author: xdz
# @Time :2020/6/9 19:23
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message


#异步执行发送邮件
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


# 发送电子邮件
def send_mail(to, subject, template, **kwargs):
    # python eamil
    msg = Message('[漂书]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 通过该方法获得真实的flask app对象
    app = current_app._get_current_object()
    # args传入一个list，里面的具体值是target中的目标函数的参数
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
