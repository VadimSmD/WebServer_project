from flask import Flask, request, send_from_directory
from GmailCode import send_code_to, send_report
from data.Users import User
from data.Emails import Email
from data.Files import File
from hashlib import sha3_512
from form_classes import registration
from form_classes import authorization
from form_classes import emailform
from form_classes import fileform
from flask import redirect, session, render_template
from db import db_session
from flask_login import LoginManager, login_user, current_user
from TypicalChecks import password_check
import datetime
import flask
from flask_wtf.csrf import CSRFProtect, CSRFError
from sqlalchemy.sql.expression import func
import subprocess
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ud8hJwI_DarkMail'
app.config['UPLOAD_FOLDER'] = 'files'
csrf = CSRFProtect()
csrf.init_app(app)
app.config['WTF_CSRF_SECRET_KEY.'] = 'KUnso8+aajwHGe,cai123djj;f'
app.config.update(SESSION_COOKIE_SECURE=True,
                  SESSION_COOKIE_HTTPONLY=True,
                  SESSION_COOKIE_SAMESITE='Lax')

db_session.global_init("db/users.db")
db_sess = db_session.create_session()

subprocess.call('mkdir db\\backups', shell=True, stdout=False)
comand = f'copy db\\users.db db\\backups\\copy_{str(datetime.datetime.now()).replace(" ", "_").replace(":", "_")}.db'
subprocess.call(comand, shell=True, stdout=False)

RegForm = registration.RegForm
LogForm = authorization.LoginForm
EForm = emailform.EmailForm
FForm = fileform.FileForm
login_manager = LoginManager()
login_manager.init_app(app)
try:
    os.remove('log404.txt')
except FileNotFoundError:
    pass
with open('log404.txt', 'a') as file:
    file.write('404: 0')

try:
    os.remove('reports_sended.txt')
except FileNotFoundError:
    pass
with open('reports_sended.txt', 'a') as file:
    file.write('0')

try:
    os.remove('log405.txt')
except FileNotFoundError:
    pass
with open('log405.txt', 'a') as file:
    file.write('405: 0')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    send_report('Unknown csrf token')
    return render_template('csrf_handler.html', reason=e.description), 400


@app.errorhandler(404)
def page_not_found(e):
    create = 0
    with open('log404.txt', 'r') as file:
        data = file.readlines()
        index = -1
        for l in data:
            if '404: ' in l:
                index = data.index(l)
        if index != -1:
            total = data[index].replace('404: ', '')
            if int(total) > 50:
                send_report('More than 50 404 errors')
        else:
            create = 1
    if create == 1:
        with open('log404.txt', 'a') as file:
            file.write('404: 1')
    if create == 0:
        try:
            os.remove('log404.txt')
        except FileNotFoundError:
            pass
        with open('log404.txt', 'a') as file:
            file.write('404: ' + str(int(total) + 1))
    return render_template('404.html'), 404


@app.errorhandler(400)
def page_not_found(e):
    return render_template('400.html'), 400


@app.errorhandler(405)
def page_not_found(e):
    create_405 = 0
    with open('log405.txt', 'r') as file:
        data = file.readlines()
        index = -1
        for l in data:
            if '405: ' in l:
                index = data.index(l)
        if index != -1:
            total = data[index].replace('405: ', '')
            if int(total) > 20:
                send_report('''Strange activity on the server''')
        else:
            create_405 = 1
    if create_405 == 1:
        with open('log405.txt', 'a') as file:
            file.write('405: 1')
    if create_405 == 0:
        try:
            os.remove('log405.txt')
        except FileNotFoundError:
            pass
        with open('log405.txt', 'a') as file:
            file.write('405: ' + str(int(total) + 1))
    return render_template('405.html'), 405


@app.errorhandler(500)
def page_not_found(e):
    send_report(str(e))
    return render_template('500.html'), 500


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        stage = session.get('QnaIb35', 0)
        if form.password.data == form.password_rep.data and password_check(form.password.data):
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if not user:
                if stage == 0:
                    code = send_code_to(form.email.data)
                    code = sha3_512(bytearray(code, 'utf-8')).hexdigest()
                    session['JKD9s8'] = code
                    session['QnaIb35'] = 1
                    return render_template('regform.html', title='Код регистрации', form=form, wp=2,
                                           mail_pr=form.email.data,
                                           pas_pr=form.password.data, pas_rep_pr=form.password_rep.data,
                                           nick_pr=form.name.data, addition='Зарегистрироваться')

                if stage == 1:
                    if sha3_512(bytearray(form.cod.data, 'utf-8')).hexdigest() == session.get('JKD9s8', 0):
                        db_sess = db_session.create_session()
                        user = db_sess.query(User).filter(User.name == form.name.data).first()
                        if user is None:
                            new_user = User(name=form.name.data, email=form.email.data,
                                            hashed_password=(sha3_512(bytearray(form.password.data, 'utf-8'))).hexdigest(),
                                            ip=flask.request.remote_addr)
                            db_sess.add(new_user)
                            db_sess.commit()
                            session['QnaIb35'] = 0
                        return redirect('/')
                    return render_template('regform.html', title='Регистрация', form=form, wp=0,
                                           addition='Ввести код регистрации')
            else:
                return render_template('regform.html', title='Регистрация', form=form, wp=3,
                                       addition='Ввести код регистрации')

        else:
            return render_template('regform.html', title='Регистрация', form=form, wp=1,
                                   addition='Ввести код регистрации')

    return render_template('regform.html', title='Регистрация', form=form, wp=0, addition='Ввести код регистрации')


@app.route('/login', methods=['GET', 'POST'])
def log():
    form = LogForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.hashed_password == sha3_512(bytearray(form.password.data, 'utf-8')).hexdigest():
            login_user(user, remember=False)
            return redirect('/myinbox')
        else:
            return render_template('loginform.html', title='Авторизация', form=form,
                                   addition='Войти в киберпространство.',
                                   w=1)
    return render_template('loginform.html', title='Авторизация', form=form, addition='Войти в киберпространство.', w=0)


@app.route('/index')
@app.route('/')
def main():
    return render_template('base.html', title='DarkMail')


@app.route('/sended')
def get_my_mails():
    if current_user.is_authenticated:
        mails = []
        db_sess = db_session.create_session()
        letters = sorted(db_sess.query(Email).filter(Email.sender_id == current_user.id).all(),
                         key=lambda x: (x.date, x.sender_id, x.thema),
                         reverse=True)
        for l in letters:
            mails.append(['/mail/' + str(l.id), 'Вы', l.thema, l.date])
        return render_template('sended_mails.html', show=1, data=mails)
    else:
        return render_template('sended_mails.html', show=0)


@app.route('/myinbox')
def mails():
    if current_user.is_authenticated:
        mails = []
        db_sess = db_session.create_session()
        letters = sorted(db_sess.query(Email).filter(Email.reciever_id == current_user.id).all(),
                         key=lambda x: (x.date, x.sender_id, x.thema),
                         reverse=True)
        for l in letters:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == l.sender_id).first()
            mails.append(['/mail/' + str(l.id), user.name, l.thema, l.date])
        return render_template('mainform.html', title='DarkMail', show=1, ids=mails)
    else:
        return render_template('mainform.html', title='DarkMail', show=0)


@app.route('/send', methods=['GET', 'POST'])
def s():
    form = EForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            reciever = db_sess.query(User).filter(User.name == form.name.data).first()
            if reciever:
                new_mail = Email(reciever_id=reciever.id, content=form.text.data, sender_id=current_user.id,
                                 thema=form.thema.data, date=datetime.datetime.now())
                db_sess.add(new_mail)
                db_sess.commit()
            return redirect('/myinbox')
        return render_template('sendform.html', title='DarkMail', show=1, form=form)
    else:
        return render_template('sendform.html', title='DarkMail', show=0)


@app.route('/send_file_to', methods=['GET', 'POST'])
def send_file():
    form = FForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            reciever = db_sess.query(User).filter(User.name == form.name.data).first()
            f = request.files['file']
            name = ((str(form.file.data).split(' '))[1].replace("'", ''))
            index = name.index('.')
            name = name[index:]
            max_id = db_sess.query(func.max(File.id)).first()[0]
            if max_id is None:
                max_id = 0
            if reciever:
                info = f.read()
                new_file = File(reciever_id=reciever.id, sender_id=current_user.id, date=datetime.datetime.now(),
                                ext=name)
                with open(f'files/{str(max_id)}{name}', 'wb') as file:
                    file.write(info)
                db_sess.add(new_file)
                db_sess.commit()
                return redirect('/myinbox')
            else:
                return redirect('/myinbox')
        return render_template('file_send_form.html', show=1, form=form, title='DarkMail')
    else:
        return render_template('file_send_form.html', show=0, title='DarkMail')


@app.route('/myfiles')
def get_files():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        files = sorted(db_sess.query(File).filter(File.reciever_id == current_user.id).all(),
                       key=lambda x: (x.date, x.sender_id),
                       reverse=True)
        dat = []
        for file in files:
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.id == file.sender_id).first()
            dat.append(['/file/' + str(file.id), user.name, file.date])
        return render_template('recieved_files.html', show=1, title='DarkMail', data=dat)
    else:
        return render_template('recieved_files.html', show=0, title='DarkMail')


@app.route('/mail/<int:code>')
def get_mail(code):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        mail = db_sess.query(Email).filter(Email.id == code).first()
        user = db_sess.query(User).filter(User.id == mail.sender_id).first()
        sender = user.name
        date = mail.date
        thema = mail.thema
        content = list(mail.content)
        if len(content) > 120:
            srezs = len(content) // 120
            start = 120
            for i in range(srezs):
                content.insert(start, '\n')
                start += 120
        content = ''.join(content)

        return render_template('letterform.html', title='DarkMail', show=1, sender=sender, date=date, thema=thema,
                               content=content)
    else:
        return render_template('letterform.html', title='DarkMail', show=0)


@app.route('/file/<int:code>', methods=['GET', 'POST'])
def get_file(code):
    code1 = code-1
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        f = db_sess.query(File).filter(File.id == code).first()
        if f is not None:
            if f.reciever_id == current_user.id:
                filename = str(code1) + f.ext
                return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
            else:
                return render_template('base.html', title='DarkMail')
        else:
            return render_template('base.html', title='DarkMail')
    else:
        return render_template('letterform.html', title='DarkMail', show=0)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
