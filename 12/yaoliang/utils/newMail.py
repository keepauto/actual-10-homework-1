# coding:utf-8
# flask-mail插件

from app import app
from flask_mail import Mail,Message
from threading import Thread
import os

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'smtp.example.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or'123456'

mail = Mail(app)

def send_async_email(app,msg):
    with app.app_content():
	mail.send(mag)

@app.route('/mail')
def mail():
    msg = Message('Hi',sender='me@example.com',recopients=['he@example.com'])
    msg.html = '<b>hello world!</b>'

    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return 'send successfully'

