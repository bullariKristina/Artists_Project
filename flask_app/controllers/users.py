import datetime
import math
import random
import smtplib
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.job import Job

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from .env import ADMINEMAIL
from .env import PASSWORD


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return redirect('/logout')

@app.route('/registerpage')
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('registration.html')

@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    #Check if another user has the same email
    if not request.form.get('status'):
        status=""
    else:
        status=request.form.get('status')
    data1 = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password'],
        'status': status,
        'profession': request.form['profession'],
        'is_verified': 0,
    }
    if User.get_user_by_email(request.form):
        flash('This email already exists. Try another one.', 'emailSignUp')
        return redirect(request.referrer)
    #Validate the user
    if not User.validate_user(data1):
        return redirect(request.referrer)
    
    string = '0123456789ABCDEFGHIJKELNOPKQSTUV'
    vCode = ""
    length = len(string)
    for i in range(8) :
        vCode += string[math.floor(random.random() * length)]
    verificationCode = vCode
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'status': status,
        'profession': request.form['profession'],
        'is_verified': 0,
        'verificationCode': verificationCode
    }
    User.create_user(data)
    return redirect('/')

@app.route('/loginpage')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('login.html')


@app.route('/login', methods = ['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    user = User.get_user_by_email(request.form)
    #Checks if there is a user with that email
    if not user:
        flash('This email does not exist.', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Your password is wrong!', 'passwordLogin')
        return redirect(request.referrer)
    #Checks if there is a user with that email
    session['user_id'] = user['id']
    return redirect('/')

@app.route('/verify/email')
def verifyEmail():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    if user['isVerified'] == 1:
        return redirect('/dashboard')
    return render_template('verifyEmail.html', loggedUser = user)

@app.route('/profile')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    loggedUserData = {
        'user_id': session['user_id']
    } 
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/logout')
    return render_template('profile.html', loggedUser = User.get_user_by_id(loggedUserData))

@app.route('/editprofile')
def editProfile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('editProfile.html', loggedUser = User.get_user_by_id(data))

@app.route('/edit/user/profile', methods=['POST'])
def edit_user():
    if 'user_id' not in session:
        return redirect('/')
    if not User.validate_user_on_update(request.form):
        return redirect(request.referrer)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        User.edit_user(data)
        return redirect(request.referrer)
    return redirect(request.referrer)

@app.route('/deleteprofile')
def deleteProfile():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    if loggedUser['id'] == session['user_id']:
        Job.delete_all_user_jobs(data)
        User.delete_user(data)
        return redirect('/logout')
    return redirect(request.referrer)

@app.route('/create')
def create():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    return render_template('create.html', loggedUser = User.get_user_by_id(data))



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginpage')
