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

# Check if the format is right 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dashboard')
def dashboard():
    if 'user_id'in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        return render_template('dashboard.html', loggedUser = loggedUser)
    return redirect('/')

@app.route('/create/job', methods = ['POST'])
def createJob():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'salary': request.form['salary'],
        'user_id': session['user_id']
    }
    if not Job.validate_job(data):
        return redirect(request.referrer)
    Job.create_job(data)
    return redirect('/')


@app.route('/create/proposal', methods = ['POST'])
def createProposal():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'skill1': request.form['skill1'],
        'skill2': request.form['skill2'],
        'skill3': request.form['skill3'],
        'user_id': session['user_id']
    }   
    if not Proposal.validate_proposal(data):
        return redirect(request.referrer)
    Proposal.create_proposal(data)
    return redirect(request.referrer)

@app.route('/jobproposals')
def jobProposal():
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id']
        }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/')
    return render_template('jobproposals.html', loggedUser=loggedUser, jobs = Job.get_jobs(), proposals = Proposal.get_proposals())


@app.route('/job/<int:id>')
def viewJob(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'job_id': id
    }
    loggedUser = User.get_user_by_id(data)
    job = Job.get_job_by_id(data)
    creator_id = job['user_id']
    userid = {
        'user_id': creator_id
    }
    return render_template('view.html', job = job, loggedUser = loggedUser, creator = User.get_user_by_id(userid))

@app.route('/proposal/<int:id>')
def viewProposal(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'proposal_id': id
    }
    loggedUser = User.get_user_by_id(data)
    proposal = Proposal.get_proposal_by_id(data)
    creator_id = proposal['user_id']
    userid = {
        'user_id': creator_id
    }
    return render_template('view.html', proposal = proposal, loggedUser = loggedUser, creator = User.get_user_by_id(userid))


@app.route('/apply/<int:id>')
def apply(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'job_id': id
    }
    allUsersWhoApplied = Job.get_users_who_applied(data)
    if session['user_id'] not in allUsersWhoApplied:
        Job.apply(data)
    return redirect(request.referrer)


@app.route('/delete/<int:id>')
def deleteJob(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'job_id': id
    }
    loggedUser = User.get_user_by_id(data)
    job = Job.get_job_by_id(data)
    if loggedUser['id'] != job['user_id']:
        return redirect(request.referrer)
    Job.delete_job(data)
    return redirect(request.referrer)
    

@app.route('/proposal/admin/<int:id>')
def suitablePeople(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id'],
        'proposal_id': id
    }
    loggedUser = User.get_user_by_id(data)
    proposal = Proposal.get_proposal_by_id(data)
    creatorId = {
        'user_id': proposal['user_id']
    }
    if loggedUser['admin'] == 1:
        users = Proposal.get_users_for_proposal(data)
        return render_template('users.html', users = users, loggedUser = loggedUser, creator = User.get_user_by_id(creatorId))
    return redirect('/')
    

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
        if not request.files['image']:
            flash('Image is required!', 'portfolioImage')
            return redirect(request.referrer)
   
        image = request.files['image']
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
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        portfolioUser = User.get_user_portfolio(data)
        if not portfolioUser:
            Portfolio.create_portfolio(data)
            portfolioUser = User.get_user_portfolio(data)
            data1 = {
                'image': filename1,
                'portfolio_id': portfolioUser['id']
            }
            Image.create_image(data1)
            return redirect(request.referrer)
        data2 = {
            'description': request.form['description'],
            'image': filename1,
            'portfolio_id': portfolioUser['id']
        }
        Portfolio.update_portfolio(data2)
        Image.create_image(data2)
        return redirect(request.referrer)
    return redirect('/')

@app.route('/portfolio/<int:id>')
def userPortfolio(id):
    if 'user_id'in session:
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
        return render_template('portfolio.html', portfolio = portfolio, images = images, loggedUser = loggedUser)
    return redirect('/')


    
    