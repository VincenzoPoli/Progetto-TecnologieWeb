from flask_mail import Message
from app import app, mail
from flask import render_template
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


def send_reset_password_email(user):
    token = user.get_reset_password_token()
    send_email('[Newspaper] Reimposta password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token)
               )


def send_registration_summary_email(user):
    send_email('[Newspaper] Conferma di registrazione',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/registered.txt', user=user),
               html_body=render_template('email/registered.html', user=user)
               )


def send_edited_password_summary_email(user):
    send_email('[Newspaper] Password modificata',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/edited_password.txt', user=user),
               html_body=render_template('email/edited_password.html', user=user)
               )


def send_edited_profile_summary_email(user):
    send_email('[Newspaper] Profilo aggiornato',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/edited_profile.txt', user=user),
               html_body=render_template('email/edited_profile.html', user=user)
               )

def send_deleted_profile_summary_email(user):
    send_email('[Newspaper] Profilo eliminato',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/deleted_user.txt', user=user),
               html_body=render_template('email/deleted_user.html', user=user)
               )