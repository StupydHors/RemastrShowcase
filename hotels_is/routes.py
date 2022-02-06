from datetime import timedelta

from flask import render_template, url_for, redirect, request, session
from flask.helpers import flash
from flask_login import login_user, current_user, logout_user

from hotels_is import app
from hotels_is.utils.passwords import *
from .models import *


# Route to index page
@app.route('/')
def index():
    if current_user.is_authenticated or current_user.is_anonymous:
        return redirect(url_for('everyone.offering'))
    else:
        return render_template('login.html')


# Route to login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    failed = True if request.args.get('failed') else False
    if request.method == "GET":
        return render_template('login.html', failed=failed)
    elif request.method == "POST":
        try:
            uzivatel = Uzivatel.query.filter_by(email=request.form['email']).first()
            if uzivatel and verify_password(uzivatel.password, request.form['password']):
                login_user(uzivatel)
                return redirect(url_for('index'))
        except Exception as e:
            print(e)
        return redirect(url_for('login', failed=True))


# Route to register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        formdata = session.get('formdata', None)
        if formdata:
            return render_template('register.html', formdata=formdata)
        return render_template('register.html')
    elif request.method == "POST":

        uzivatel = Uzivatel.query.filter_by(email=request.form['email']).first()
        # test if email is already registered
        if not uzivatel:  
            try:
                email = request.form['email']
                name = request.form['name']
                phone_number = request.form['phone_number']
                password = request.form['password']
                uzivatel = Uzivatel(email=email, password=hash_password(password), role="Zákazník", name=name, phone_number=phone_number)
                db.session.add(uzivatel)
                db.session.commit()
                session.pop('formdata')
                login_user(uzivatel)
            except Exception as e:
                pass
        else:
            flash("Email je již zabraný.")
            session['formdata'] = request.form
            return redirect(url_for('register'))

    return redirect(url_for('index'))


# Route to logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


# Session timetout after 150 minutes
@app.before_request
def session_timeout():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=150)
