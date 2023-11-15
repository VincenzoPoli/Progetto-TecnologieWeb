import os
basedir = os.path.abspath(os.path.dirname(__file__))  # directory principale dell'applicazione
class Config(object):
    # os.environ.get controlla la var d'ambiente specificata tra parentesi e se non settata la chiave è quella fornita dopo or
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQALCHEMY_TRACK_MODIFICATIONS = False # disabilita la segnalazione all'applicazione ogni volta che si sta per apportare una modifica nel database
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'progettotecweb0@gmail.com'
    MAIL_PASSWORD = 'orna xpvh eigt lsez'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ADMINS = ['progettotecweb0@gmail.com']
    POSTS_PER_PAGE = 1
    ARTICLES_PER_PAGE = 16
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"