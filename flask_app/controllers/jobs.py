from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.job import Job
from flask_app.models.proposal import Proposal


@app.route('/dashboard')
def all_recipes():
    if 'user_id' in session:
        loggedUserData = {
            'user_id': session['user_id'],
        }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/')
    return render_template('dashboard.html', loggedUser=loggedUser)


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
            'user_id': session['user_id'],
        }
    loggedUser = User.get_user_by_id(loggedUserData)
    if not loggedUser:
        return redirect('/')
    return render_template('jobproposals.html', loggedUser=loggedUser, jobs = Job.get_jobs())

# @app.route('/recipes/<int:id>')
# def viewRecipe(id):
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'user_id': session['user_id'],
#         'recipe_id': id
#     }
#     loggedUser = User.get_user_by_id(data)
#     recipe = Recipe.get_recipe_by_id(data)
#     return render_template('viewRecipe.html', recipe = recipe, loggedUser = loggedUser)


@app.route('/jobs/delete/<int:id>')
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
    

    
    