import smtplib
from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.job import Job
from flask_app.models.proposal import Proposal
from flask_app.models.portfolio import Portfolio
from flask_app.models.image import Image
from datetime import datetime
import os
from .env import UPLOAD_FOLDER
from .env import ALLOWED_EXTENSIONS
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request
from flask_mail import Mail, Message

from .env import ADMINEMAIL
from .env import PASSWORD

# Check if the format is right 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/portfolio')
def portfolio():
    if 'user_id'in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('addPortfolio.html', loggedUser = loggedUser, portfolio = User.get_user_portfolio(loggedUserData))
    return redirect('/')


@app.route('/create/portfolio', methods = ['POST'])
def createPortfolio():
    if 'user_id' in session:
        if not Portfolio.validate_portfolio(request.form):
            return redirect(request.referrer)
        data = {
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        portfolioUser = User.get_user_portfolio(data)
        if not portfolioUser:
            Portfolio.create_portfolio(data)
            portfolioUser = User.get_user_portfolio(data)
            return redirect(request.referrer)
        data2 = {
            'description': request.form['description'],
            'portfolio_id': portfolioUser['id']
        }
        Portfolio.update_portfolio(data2)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/create/work', methods = ['POST'])
def createWork():
    if 'user_id' in session:
        user = {
            'user_id': session['user_id']
        }
        portfolioUser = User.get_user_portfolio(user)
        if portfolioUser:
            user = {
                'user_id': portfolioUser['user_id']
            }
            userData = User.get_user_by_id(user)
            if userData['status'] == 'artist':
                if not Image.validate_image(request.form):
                    return redirect(request.referrer)
                image = request.files['image']
                if not image:
                    flash('Image is required!', 'portfolioImage')
                    return redirect(request.referrer)
                if not allowed_file(image.filename):
                    flash('Image should be in png, jpg, jpeg format!', 'postImage')
                    return redirect(request.referrer)
                if image and allowed_file(image.filename):
                    filename1 = secure_filename(image.filename)
                    time = datetime.now().strftime("%d%m%Y%S%f")
                    time += filename1
                    filename1 = time
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                data = {
                    'caption': request.form['caption'],
                    'image': filename1,
                    'portfolio_id': portfolioUser['id']
                }
                Image.add_work(data)

            elif userData['status'] == 'it':
                if not Image.validate_image(request.form):
                    return redirect(request.referrer)
                image = request.form['image']
                if not image:
                    flash('Image is required!', 'portfolioImage')
                    return redirect(request.referrer)
                data = {
                    'caption': request.form['caption'],
                    'image': request.form['image'],
                    'portfolio_id': portfolioUser['id']
                }
                Image.add_work(data) 
        if not portfolioUser:
            flash('Please, first add a description to your portfolio. That way we can start setting up your portfolio.', 'addDescription')
            return redirect(request.referrer)
        return redirect(f"/portfolio/{portfolioUser['id']}")
    return redirect('/')

@app.route('/portfolio/<int:id>')
def userPortfolio(id):
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        data = {
            'user_id': id
        }
        portfolio = User.get_user_portfolio(data)
        images = Portfolio.all_images(data)
        return render_template('portfolio.html', portfolio = portfolio, images = images, loggedUser = loggedUser, portfolioUser = User.get_user_by_id(data))
    return redirect('/')

@app.route('/edit/work/<int:id>')
def editWork(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'image_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('editWork.html', loggedUser = loggedUser, work = Image.get_image_by_id(data))

@app.route('/edit/work/<int:id>', methods=['POST'])
def editImage(id):
    if 'user_id' in session:
        user = {
            'user_id': session['user_id']
        }
        loggedUser = User.get_user_by_id(user)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        if not Image.validate_image(request.form):
            return redirect(request.referrer)
        data = {
            'caption': request.form['caption'],
            'image_id': id
            }
        image = Image.get_image_by_id(data)
        creatorId = {
            'user_id': image['user_id'] 
        }
        #Get the creater of that image and check if he is the same as the one in session
        user = User.get_user_by_id(creatorId)
        if user['id'] == session['user_id']:
            Image.edit_image(data)
            return redirect(f"/portfolio/{user['id']}")
        return redirect(request.referrer)
    return redirect(request.referrer)

        
@app.route('/delete/work/<int:id>')
def deleteWork(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'image_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        image = Image.get_image_by_id(data)
        creatorId = {
            'user_id': image['user_id'] 
        }
        #Get the creater of that image and check if he is the same as the one in session
        user = User.get_user_by_id(creatorId)
        if user['id'] == session['user_id']:
            Image.delete_image(data)
            return redirect(request.referrer)
        return redirect(request.referrer)
    return redirect('/')
