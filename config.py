import os
basedir = os.path.abspath(os.path.dirname(__file__))  # directory principale dell'applicazione
class Config(object):
    # os.environ.get controlla la var d'ambiente specificata tra parentesi e se non settata la chiave è quella fornita dopo or
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQALCHEMY_TRACK_MODIFICATIONS = False # disabilita la segnalazione all'applicazione ogni volta che si sta per apportare una modifica nel database
    POSTS_PER_PAGE = 1
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"