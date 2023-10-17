from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    db_name = 'db_project'
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.passowrd = data['password']
        self.status = data['status']
        self.profession = data['profession']
        self.is_verified = data['is_verified']
        self.verificationCode = data['verificatonCode']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, status, profession, is_verified, verificationCode) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(status)s, %(profession)s, %(is_verified)s, %(verificationCode)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
   
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE users SET is_verified = 1 WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    #Checks if there is a user with that email (needed for registration process)

    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE users SET  verificationCode = %(verificationCode)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
   
    #All information of all users
    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(cls.db_name).query_db(query)
        users= []
        if results:
            for user in results:
                users.append(user)
            return users
        return users
    

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    

    # #List of all recipes a given user has liked
    # @classmethod
    # def get_one_user_liked_recipes(cls, data):
    #     query = "SELECT likes.recipe_id as id from likes where user_id = %(user_id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query, data)
    #     likedRecipes = []
    #     if results:
    #         for like in results:
    #             likedRecipes.append( like['id'] )
    #         return likedRecipes
    #     return likedRecipes
    
    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'password')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'confirmPassword')
            is_valid = False
        if  len(user['status'])<1:
            flash('Please state your status', 'status')
            is_valid = False
        if len(user['profession'])< 2:
            flash('Profession must be more than 2 characters', 'profession')
            is_valid = False
        return is_valid
    
    #It valides when user tries to update 
    @staticmethod
    def validate_user_on_update(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailSignUp')
            is_valid = False
        if len(user['first_name'])< 2:
           flash('First name must be more than 2 characters', 'firstName')
           is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False 
        else:
            flash('User updated successfully!!', 'successfullUpdate')    
        return is_valid
    