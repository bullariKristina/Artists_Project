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
        return render_template('dashboard.html', loggedUser = loggedUser, images3 = Image.get_3_last_images(), jobs = Job.get_4_last_jobs(), its = User.get_4_it())
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
    return render_template('view.html', job = job, loggedUser = loggedUser, creator = User.get_user_by_id(userid), allUsersWhoApplied = Job.get_users_who_applied(data))

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

@app.route('/contact')
def contactUs():
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
        loggedUser = User.get_user_by_id(loggedUserData)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
    return render_template('contact.html', loggedUser = User.get_user_by_id(loggedUserData))
    

@app.route('/job/delete/<int:id>')
def delete_job(id):
    if 'user_id' in session:
        data = {
            'user_id': session['user_id'],
            'job_id': id
        }
        loggedUser = User.get_user_by_id(data)
        if loggedUser['setUp'] == 0:
            return redirect('/complete/register')
        if loggedUser['is_verified'] == 0:
            return redirect('/verify/email')
        job = Job.get_job_by_id(data)
        creatorId = {
            'user_id': job['user_id'] 
        }
        #Get the creater of that job and check if he is the same as the one in session
        user = User.get_user_by_id(creatorId)
        if user['id'] == session['user_id']:
            Job.delete_job(data)
            return redirect('/jobproposals')
        return redirect(request.referrer)
    return redirect('/')

        
