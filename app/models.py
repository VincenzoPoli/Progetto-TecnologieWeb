from datetime import datetime, timezone
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    avatar_link = db.Column(db.String())
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    role = db.Column(db.String(), default='utente')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        if self.avatar_link is not None:
            return self.avatar_link
        else:
            # poiché il supporto MD5 in Python funziona su byte e non su stringhe, codifichiamo la stringa come byte prima di passarla alla funzione hash
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            # {} è l'hash della email (digest), d=identicon genera avatar geometrici e s={} è il size specificato
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text())
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    author = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(75), unique=True)
    subtitle = db.Column(db.String(150))
    body = db.Column(db.Text())
    head_img = db.Column(db.String())
    timeStamp = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))
    author = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def head_image(self):
        return self.head_img

    def __repr__(self):
        return '<Article {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(id)
