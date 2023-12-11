from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Portfolio:
    db_name = 'artistProject'
    def __init__( self , data ):
        self.id = data['id']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def all_images(cls, data):
        try:
            query = 'SELECT images.id as id, images.image as image, images.caption as caption FROM users JOIN portfolios ON users.id = portfolios.user_id JOIN images ON portfolios.id = images.portfolio_id WHERE users.id = %(user_id)s;' 
            results = connectToMySQL(cls.db_name).query_db(query, data)
            if results:
                return results
            else:
                return []
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
    
    @classmethod
    def get_images(cls, data):
        query = "SELECT * FROM images WHERE portfolio_id = %(portfolio_id)s;" 
        results = connectToMySQL(cls.db_name).query_db(query, data)
        images = []
        if results:
            for image in results:
                images.append(image)
            return images
        return images  
    
    @classmethod
    def list_users_with_portfolios(cls):
        query = 'SELECT DISTINCT portfolios.user_id FROM portfolios JOIN users ON users.id = portfolios.user_id;;' 
        results = connectToMySQL(cls.db_name).query_db(query)
        users = []
        if results:
            for user in results:
                users.append(user['user_id'])
            return users
        return users

    @classmethod
    def create_portfolio(cls, data):
        query = "INSERT INTO portfolios (description, user_id) VALUES (%(description)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def update_portfolio(cls, data):
        query = "UPDATE portfolios SET description = %(description)s WHERE portfolios.id = %(portfolio_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_portfolio(data):
        is_valid = True
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'portfolioDescription')
            is_valid = False
        else:
            flash('Portfolio successfully upated!', 'portfolioSuccess')
        return is_valid
    