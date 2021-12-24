import json
import random

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session, app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, send_comms
from .models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        mob_mail = request.form.get('mob_mail')
        password = request.form.get('password')
        user_otp = request.form.get('otp')
        if mob_mail.isdigit():
            user = User.query.filter_by(mob=int(mob_mail)).first()
        else:
            user = User.query.filter_by(email=mob_mail).first()
        if user:
            if user_otp:
                user_otp = int(user_otp)
                print(f'OTP Generated: {user.last_otp}')
                print(f'OTP user_otp: {user_otp}')
            # print(user)
            # print(f'User pwd: {user.password}')
            # print(f'Password: {password}')
            # print(f'Check hash: {check_password_hash(user.password, password)}')

            if (check_password_hash(user.password, password)) or user_otp == user.last_otp:
                flash('Logged in successfully!', category='success')
                session['user'] = user.email
                print(session)
                login_user(user, remember=True)
                print(current_user.email)
                return redirect(url_for('views.home'))
            else:
                if not user_otp and not check_password_hash(user.password, password):
                    flash('Incorrect password, try again.', category='error')
                elif user_otp != user.last_otp:
                    flash('Incorrect OTP, try again.', category='error')

        else:
            flash('Email Id or Mobile number does not exist.', category='error')

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        mob_mail = request.form.get('mob_mail')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_otp = int(request.form.get('otp'))
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            if mob_mail.isalnum():
                user = User.query.filter_by(mob=int(mob_mail)).first()
            else:
                user = User.query.filter_by(email=mob_mail).first()
            if user:
                print(f'OTP Generated: {user.last_otp}')
                print(f'OTP user_otp: {user_otp}')
                print(f'password1: {password1}')
                print(f'password2: {password2}')
                if user_otp != user.last_otp:
                    flash('Incorrect OTP, try again.', category='error')
                else:
                    user.password = generate_password_hash(password1, method='sha256')
                    db.session.commit()
                    login_user(user, remember=True)
                    flash('Password Changed Successfully!', category='success')
                    return redirect(url_for('views.home'))
            else:
                flash('Email Id or Mobile number does not exist.', category='error')
                return redirect(url_for('auth.sign-up'))

    return render_template("forget_password.html", user=current_user)


@auth.route('/generate_otp', methods=['POST'])
def generate_otp():
    ip = json.loads(request.data)
    mob_mail = ip['mob_mail']
    print(mob_mail)
    if mob_mail.isdigit():
        user = User.query.filter_by(mob=int(mob_mail)).first()
    else:
        user = User.query.filter_by(email=mob_mail).first()
    if user:
        otp = random.randint(100000, 999999)
        otp_latest = otp
        content = 'Your OTP for log in is ' + str(otp_latest)
        print(f'OTP Generated in Auth Function: {otp_latest}')
        user.last_otp = otp_latest
        db.session.commit()
        send_comms.send_sms(content, user.mob)
        send_comms.send_mail(user.email, 'OTP for Password Reset', content)
        flash('OTP Generated.', category='success')
        return jsonify({})
    else:
        flash('Email Id or Mobile number does not exist. Please Create an Account', category='error')
        data_return = {'error': 'failure'}
        return jsonify(data_return)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        mob = request.form.get('mob')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, mob=mob, password=generate_password_hash(
                password1, method='sha256'), first_name=first_name, last_name=last_name)
            db.session.add(new_user)
            db.session.commit()
            # session['user'] = new_user.email
            # print(session)
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
