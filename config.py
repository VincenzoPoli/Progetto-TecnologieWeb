import os
basedir = os.path.abspath(os.path.dirname(__file__))  # directory principale dell'applicazione
class Config(object):
    # os.environ.get controlla la var d'ambiente specificata tra parentesi e se non settata la chiave è quella fornita dopo or
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQALCHEMY_TRACK_MODIFICATIONS = False # disabilita la segnalazione all'applicazione ogni volta che si sta per apportare una modifica nel database

    '''MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')'''

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'progettotecweb0@gmail.com'
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    ADMINS = ['progettotecweb0@gmail.com']
    POSTS_PER_PAGE = 1
    ARTICLES_PER_PAGE = 16
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"