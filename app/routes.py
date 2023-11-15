from flask import render_template, flash, redirect, url_for, request, session
from app import app, login, db
from app.email import send_reset_password_email, send_registration_summary_email, send_edited_password_summary_email, send_edited_profile_summary_email, send_deleted_profile_summary_email
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, ArticleForm, EditArticleForm, \
    AssignRoleForm, EditPasswordForm, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Article
from werkzeug.utils import secure_filename
from datetime import datetime

# redireziona all'endpoint di login se la pagina richiede l'accesso per essere visualizzata
login.login_view = 'login'


@app.route('/')
@app.route('/index')
def index():
    # grazie a session sarà possibile ritornare alla pagina precedente quando si sottomette un form come ad esempio quello di login o modifica commenti
    session['url'] = url_for('index')
    articles = Article.query.order_by(Article.timeStamp.desc()).all()
    first_row = articles[:2]
    second_row = articles[2:5]
    third_row = articles[5:7]
    return render_template('index.html', title='Home', first_row=first_row, second_row=second_row, third_row=third_row)


@app.route('/explore')
def explore():
    # RICORDA
    # .get(key, default=None, type=None)
    # paginate(page, per_page, error_out, max_per_page)
    # Returns per_page items from page page
    current_page = 'explore'
    # grazie a session sarà possibile ritornare alla pagina precedente quando si sottomette un form come ad esempio quello di login o modifica commenti
    session['url'] = url_for('explore')
    page = request.args.get('page', 1, type=int)
    articles = Article.query.order_by(Article.timeStamp.desc()).paginate(
        page=page, per_page=app.config['ARTICLES_PER_PAGE'], error_out=False
    )
    if articles.has_next:
        next_url = url_for('explore', page=articles.next_num)
    else:
        next_url = None
    if articles.has_prev:
        prev_url = url_for('explore', page=articles.prev_num)
    else:
        prev_url = None
    first_col = articles.items[:8]
    second_col = articles.items[8:16]
    return render_template(
        'explore.html', title='Esplora',
        next_url=next_url, prev_url=prev_url,
        first_col=first_col, second_col=second_col,
        user=current_user,
        current_page=current_page
    )


@app.route('/pubislhed/<article_title>', methods=['GET', 'POST'])
def published(article_title):
    # RICORDA
    # .get(key, default=None, type=None)
    # paginate(page, per_page, error_out, max_per_page)
    # Returns per_page items from page page
    current_page = 'published'
    article = Article.query.filter_by(title=article_title).first()
    author = User.query.filter_by(username=article.author).first()
    # grazie a session sarà possibile ritornare alla pagina precedente quando si sottomette un form come ad esempio quello di login o modifica commenti
    session['url'] = url_for('published', article_title=article.title)
    page = request.args.get('page', 1, type=int)
    form = PostForm()
    date_hour = 'Articolo pubblicato il: {}/{}/{}, alle ore {}:{:02d}'.format(
        article.timeStamp.day, article.timeStamp.month, article.timeStamp.year, article.timeStamp.hour,
        article.timeStamp.minute
    )
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.username, user_id=current_user.id, article_id=article.id)
        db.session.add(post)
        db.session.commit()
        flash("Commento pubblicato!")
        return redirect(url_for('published', article_title=article_title))
    post_count = Post.query.filter_by(article_id=article.id).count()
    posts = Post.query.filter_by(article_id=article.id).order_by(Post.timeStamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    users = User.query.all()
    if posts.has_next:
        next_url = url_for('published', article_title=article_title, page=posts.next_num)
    else:
        next_url = None
    if posts.has_prev:
        prev_url = url_for('published', article_title=article_title, page=posts.prev_num)
    else:
        prev_url = None
    return render_template(
        'published.html', form=form, article=article,
        date_hour=date_hour, posts=posts.items, post_count=post_count,
        author=author, users=users,
        next_url=next_url, prev_url=prev_url,
        current_page=current_page
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():  # controlla che il form dopo il submit sia valido: restituisce false quando è invocato il metodo get
        user = User.query.filter_by(
            username=form.username.data).first()  # selezione il primo risultato con username=dato fornito dall'utente ed inviato con una richiesta post, None altrimenti
        if user is None or not user.check_password(form.password.data):  # se l'utente non esiste o la password è errata
            flash('Username o password errati.')
            return redirect(session['url'])
        login_user(user, remember=form.remember_me.data)
        return redirect(session['url'])
    return render_template('login.html', title='Accedi', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(session['url'])


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password1.data)
        db.session.add(user)
        db.session.commit()
        flash('Ti sei registrato!')
        send_registration_summary_email(user)
        return redirect(url_for('login'))
    return render_template('register.html', title='Registrati', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    current_page = 'user'
    # seleziona i dati utenti opportuni
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', title=username, user=user, current_page=current_page)


# il codice seguente verrà eseguito prima (subito prima) di una view function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    current_page = 'user'
    form = EditProfileForm()
    if form.validate_on_submit():
        if request.files:

            f = request.files['filename']
            f.save('app/static/uploads/' + secure_filename(f.filename))
            avatar_link = '/static/uploads/' + f.filename

            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.avatar_link = avatar_link
            current_user.about_me = form.about_me.data
            db.session.commit()
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.avatar_link = form.avatar_link.data
            current_user.about_me = form.about_me.data
            db.session.commit()
        send_edited_profile_summary_email(current_user)
        flash('Le tue modifiche sono state salvate.')
        return redirect(url_for('edit_profile'))
    # se arriva una richiesta GET, vengono visualizzati i dati correnti nel form, affinché sia possibile modificarli
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.avatar_link.data = current_user.avatar_link
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form, current_page=current_page)


@app.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    current_page = 'user'
    form = EditPasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password1.data)
        db.session.commit()
        flash('Passord modificata con successo!')
        send_edited_password_summary_email(current_user)
        return redirect(url_for('edit_profile'))
    return render_template('edit_password.html', form=form, current_page=current_page)


@app.route('/assign_role/<username>', methods=['GET', 'POST'])
@login_required
def assign_role(username):
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    user = User.query.filter_by(username=username).first()
    if roles[current_user.role] < 2 or roles[user.role] >= roles[current_user.role]:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))

    form = AssignRoleForm()
    if form.validate_on_submit():
        if current_user.role == 'admin':
            user.role = form.role_for_admin.data
        else:
            user.role = form.role_for_chief_editor.data
        db.session.commit()
        flash('Nuovo ruolo assegnato')
        return redirect(url_for('assign_role', username=username))
    return render_template('assign_role.html', user=user, form=form)


@app.route('/new_article', methods=['GET', 'POST'])
@login_required
def new_article():
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    if roles[current_user.role] < 1:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))

    current_page = 'new_article'
    form = ArticleForm()
    if form.validate_on_submit():
        if request.files:
            f = request.files['filename']
            f.save('app/static/uploads/' + secure_filename(f.filename))
            head_img = '/static/uploads/' + f.filename
            article = Article(title=form.title.data, subtitle=form.subtitle.data, body=form.body.data,
                              head_img=head_img, author=current_user.username, user_id=current_user.id)
        else:
            article = Article(title=form.title.data, subtitle=form.subtitle.data, body=form.body.data,
                              head_img=form.head_img.data,
                              author=current_user.username, user_id=current_user.id)
        db.session.add(article)
        db.session.commit()
        flash("Il tuo articolo è stato pubblicato!")
        flash('Immagine salvata con successo!')
        return redirect(url_for('index'))

    return render_template('article_form.html', title='Nuovo articolo', form=form, current_page=current_page,
                           user=current_user)


@app.route('/edit_article/<article_title>', methods=['GET', 'POST'])
@login_required
def edit_article(article_title):
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    article = Article.query.filter_by(title=article_title).first()
    if roles[current_user.role] < 1 or current_user.username != article.author:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))

    form = EditArticleForm()
    user = User.query.filter_by(username=article.author).first()
    if form.validate_on_submit():
        if request.files:
            f = request.files['filename']
            f.save('app/static/uploads/' + secure_filename(f.filename))
            head_img = '/static/uploads/' + f.filename
            article.title = form.title.data
            article.subtitle = form.subtitle.data
            article.body = form.body.data
            article.head_img = head_img
            db.session.commit()
        else:
            article.title = form.title.data
            article.subtitle = form.subtitle.data
            article.body = form.body.data
            article.head_img = form.head_img.data
            db.session.commit()
        flash("Il tuo articolo è stato pubblicato!")
        flash('Immagine salvata con successo!')
        return redirect(url_for('published', article_title=article.title))
    # se arriva una richiesta GET, vengono visualizzati i dati correnti nel form, affinché sia possibile modificarli
    if request.method == 'GET':
        form.title.data = article.title
        form.subtitle.data = article.subtitle
        form.body.data = article.body
        form.head_img.data = article.head_img
    return render_template('article_form.html', title='Modifica articolo', form=form, user=user)


@app.route('/delete_post/<post_id>')
@login_required
def delete_post(post_id):
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    post = Post.query.filter_by(id=post_id).first()
    if roles[current_user.role] < 1 or current_user.username != post.author:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Post eliminato con successo!')
    return redirect(session['url'])


@app.route('/delete_article/<article_id>')
@login_required
def delete_article(article_id):
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    article = Article.query.filter_by(title=article_id).first()
    if roles[current_user.role] < 1 or current_user.username != article.author:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))

    posts = Post.query.filter_by(article_id=article.id).all()
    for post in posts:
        db.session.delete(post)
    db.session.delete(article)
    db.session.commit()
    flash('Articolo eliminato con successo!')
    return redirect(url_for('index'))


@app.route('/edit_post/<post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    roles = {'admin': 3, 'capo redattore': 2, 'redattore': 1, 'utente': 0}
    post = Post.query.filter_by(id=int(post_id)).first()
    if roles[current_user.role] < 1 or current_user.username != post.author:
        flash('Non hai i permessi per compiere questa azione!')
        return redirect(url_for('index'))

    if request.method == 'POST':
        post.body = request.form['new_body']
        db.session.commit()
        flash("Commento modificato con successo!")
    return redirect(session['url'])


@app.route('/delete_user')
@login_required
def delete_user():
    posts = Post.query.filter_by(user_id=current_user.id).all()
    for post in posts:
        db.session.delete(post)
    articles = Post.query.filter_by(author=current_user.username).all()
    for article in articles:
        db.session.delete(article)
    user = User.query.filter_by(id=current_user.id).first()
    send_deleted_profile_summary_email(user)
    db.session.delete(user)
    db.session.commit()
    flash('Account cancellato con successo!')
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_password_email(user)
        flash("Se l'indirizzo email è corretto, riceverai le istruzioni per reimpostare la password.")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password1.data)
        db.session.commit()
        flash('Password reimpostata con successo!')
        return redirect(url_for('login'))
    render_template('reset_password_form.html', title='Scegli nuova password', form=form)
