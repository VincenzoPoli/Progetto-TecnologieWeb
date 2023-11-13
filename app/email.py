from flask_mail import Message
from app import app, mail
from flask import render_template


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Newspaper] Reimposta password',
               sender=app.config['ADMINS'][0],
               recipients=user.email,
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               text_html=render_template('email/reset_password.html', user=user, token=token)
               )
