from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.job import Job


# @app.route('/dashboard')
# def all_recipes():
#     if 'user_id' in session:
#         loggedUserData = {
#             'user_id': session['user_id'],
#         }
#     loggedUser = User.get_user_by_id(loggedUserData)
#     likedRecipes = User.get_one_user_liked_recipes(loggedUserData)
#     if not loggedUser:
#         return redirect('/')
#     return render_template('dashboard.html', recipes = Recipe.get_all_recipes(), loggedUser = loggedUser, likedRecipes = likedRecipes)

# @app.route('/recipes/new')
# def recipePage():
#     if 'user_id' not in session:
#         return redirect('/')
#     return render_template('addRecipe.html')

# @app.route('/create/recipe', methods = ['POST'])
# def createRecipe():
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'name': request.form['name'],
#         'description': request.form['description'],
#         'instructions': request.form['instructions'],
#         'date_made': request.form['date_made'],
#         'under_30': request.form.get('under_30', ''),
#         'user_id': session['user_id']
#     }   
#     if not Recipe.validate_recipe(data):
#         return redirect(request.referrer)
#     Recipe.create_recipe(data)
#     return redirect('/')

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


# @app.route('/recipes/delete/<int:id>')
# def deleteRecipe(id):
#     if 'user_id' not in session:
#         return redirect('/')
#     data = {
#         'user_id': session['user_id'],
#         'recipe_id': id
#     }
#     loggedUser = User.get_user_by_id(data)
#     recipe = Recipe.get_recipe_by_id(data)
#     if loggedUser['id'] != recipe['user_id']:
#         return redirect(request.referrer)
#     Recipe.delete_likes(data)
#     Recipe.delete_recipe(data)
#     return redirect(request.referrer)
    

    
    