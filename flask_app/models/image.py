from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Image:
    db_name = 'project_artist_it'
    def __init__( self , data ):
        self.id = data['id']
        self.image = data['image']
        self.portfolio_id = data['portfolio_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_image(cls, data):
        query = "INSERT INTO images (image, portfolio_id) VALUES (%(image)s, %(portfolio_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_user_images(cls, data):
        query = 'SELECT images.image AS image FROM users JOIN portfolios ON users.id = portfolios.user_id JOIN images ON portfolios.id = images.portfolio_id WHERE users.id = %(user_id)s AND portfolios.id = %(portfolio_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        jobs= []
        if results:
            for job in results:
                jobs.append(job)
            return jobs
        return jobs

    
