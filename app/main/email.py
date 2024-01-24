from flask import render_template, current_app
from app.email import send_email
from config import Config

def send_support_notification_email(user, path, projectCode):
    print("SUPPORT_EMAIL: " + Config.SUPPORT_EMAIL)
    send_email('[' + projectCode + '] New Project Created',
               sender=user.email,
               recipients=[Config.SUPPORT_EMAIL],
               text_body=render_template('email/support_request.txt',
                                         user=user, path=path),
               html_body=render_template('email/support_request.html',
                                         user=user, path=path))
