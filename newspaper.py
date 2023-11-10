from app import app, db
from app.models import User, Post


# @app.shell_context_processors crea un context shell che aggiunge l’istanza del database e models alla shell session, ma per qualche motivo sembra dia un errore
# e sembra anche non necessaria per il corretto funzionamento
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
