from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from app.models import User, Article
from flask_login import current_user


class PostForm(FlaskForm):
    post = TextAreaField(
        'Aggiungi commento', validators=[
            DataRequired(), Length(min=0, max=140)]
    )
    submit = SubmitField('Invia')


class ArticleForm(FlaskForm):
    title = TextAreaField('Titolo', validators=[Length(min=0, max=75)])
    subtitle = TextAreaField('Sottotitolo', validators=[Length(min=0, max=150)])
    body = TextAreaField(
        'Corpo articolo',
        validators=[DataRequired(), Length(min=0)],
    )
    head_img = StringField('Immagine di intestazione')
    submit = SubmitField('Pubblica articolo')

    def validate_title(self, title):
        article = Article.query.filter_by(title=title.data).first()
        if article is not None:
            raise ValidationError('Scegli un altro titolo per questo articolo.')


class EditArticleForm(FlaskForm):
    title = TextAreaField('Titolo', validators=[Length(min=0, max=75)])
    subtitle = TextAreaField('Sottotitolo', validators=[Length(min=0, max=150)])
    body = TextAreaField(
        'Corpo articolo', validators=[
            DataRequired(), Length(min=0)]
    )
    head_img = StringField('Immagine di intestazione')
    submit = SubmitField('Pubblica articolo')

    def validate_title(self, title):
        article = Article.query.filter_by(title=title.data).first()
        current_title = request.path.replace('/edit_article/', '')
        # se esiste già un articolo con quel titolo
        if article is not None:
            # e se quell'articolo non è quello corrente
            if current_title != article.title:
                raise ValidationError('Scegli un altro titolo per questo articolo.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Ricordami')
    submit = SubmitField('Accedi')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Registrati')

    def validate_username(self, username):  # WTForms considererà questa funzione un validatore personalizzato
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Utilizza un username different.')

    def validate_email(self, email):  # WTForms considererà questa funzione un validatore personalizzato
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Utilizza un indirizzo email differente.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    avatar_link = StringField('Avatar')
    about_me = TextAreaField('Su di me', validators=[Length(min=0, max=140)])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Invia')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        # se esiste già un utente con quell'username
        if user is not None:
            # e se l'utente corrente non è quell'utente
            if current_user.username != user.username:
                raise ValidationError('Scegli un altro username!')


class AssignRoleForm(FlaskForm):
    role_for_admin = SelectField('Ruolo', validators=[DataRequired()],
                                 choices=[('capo redattore', 'Capo Redattore'), ('redattore', 'Redattore'),
                                          ('utente', 'Utente')])
    role_for_chief_editor = SelectField('Ruolo', validators=[DataRequired()],
                                        choices=[('redattore', 'Redattore'), ('utente', 'Utente')])
    submit = SubmitField('Invia')

    # def validation ruolo identico


class EditPasswordForm(FlaskForm):
    password = PasswordField('Password corrente', validators=[DataRequired()])
    password1 = PasswordField('Nuova password', validators=[DataRequired()])
    password2 = PasswordField('Ripeti password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Modifica')

    def validate_password(self, password):
        if not current_user.check_password(password.data):
            raise ValidationError('Password errata!')