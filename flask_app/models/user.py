from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User():
    db_name = 'artistProject'
    def __init__(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.passowrd = data['password']
        self.status = data['status']
        self.profession = data['profession']
        self.is_verified = data['is_verified']
        self.verificationCode = data['verificatonCode']
        self.admin = data['admin']
        self.developer = data['developer']
        self.language = data['language']
        self.chargeWay = data['chargeWay']
        self.setUp = data['setUp']
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
        query = "INSERT INTO users (email, password, status, is_verified, verificationCode, setUp) VALUES (%(email)s, %(password)s, %(status)s, %(is_verified)s, %(verificationCode)s, %(setUp)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    
    @classmethod
    def create_artist(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, profession = %(profession)s, setUp = %(setUp)s, admin = %(admin)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def create_it(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, developer = %(developer)s, language = %(language)s, chargeWay = %(chargeWay)s, setUp = %(setUp)s, admin = %(admin)s WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getlastuser(cls):
        query = 'SELECT * FROM users ORDER BY created_at DESC LIMIT 1;'
        results = connectToMySQL(cls.db_name).query_db(query)
        if results:
            return results[0]
        return False
    
    @classmethod
    def activateAccount(cls, data):
        query = "UPDATE users SET is_verified = 1 WHERE users.id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)  
    
    @classmethod
    def updateVerificationCode(cls, data):
        query = "UPDATE users SET verificationCode = %(verificationCode)s WHERE users.id = %(user_id)s;"
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
    def get_id(cls, data):
        query = "SELECT id FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results['id']
        return False


    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    

    @classmethod
    def edit_user(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_user(cls, data):
        query = "DELETE FROM users WHERE id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_portfolio(cls, data):
        query = "SELECT portfolios.id, portfolios.description, portfolios.user_id FROM portfolios JOIN users ON users.id = portfolios.user_id LEFT JOIN images ON portfolios.id = images.portfolio_id WHERE users.id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False

    @classmethod
    def get_4_it(cls):
        query = "SELECT users.*, portfolios.description FROM users JOIN portfolios ON users.id = portfolios.user_id where users.status = 'it' ORDER BY users.created_at DESC LIMIT 4;"
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user)
            return users
        return users
    
    @staticmethod
    def validate_user_artist(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailArtist')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'passwordArtist')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'confirmPasswordArtist')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_user_it(user):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'emailIt')
            is_valid = False
        if len(user['password'])< 8:
            flash('Password must be more or equal to 8 characters', 'passwordIt')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('The passwords do not match',  'confirmPasswordIt')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_artist(user):
        is_valid = True
        # test whether a field matches the pattern
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
            is_valid = False
        if len(user['profession'])< 2:
            flash('Profession must be more than 2 characters', 'profession')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_it(user):
        is_valid = True
        # test whether a field matches the pattern
        if len(user['first_name'])< 2:
            flash('First name must be more than 2 characters', 'firstName')
            is_valid = False
        if len(user['last_name'])< 2:
            flash('Last name must be more than 2 characters', 'lastName')
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
    