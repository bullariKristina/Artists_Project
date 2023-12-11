from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Image:
    db_name = 'artistProject'
    def __init__( self , data ):
        self.id = data['id']
        self.image = data['image']
        self.caption = data['caption']
        self.portfolio_id = data['portfolio_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_work(cls, data):
        query = "INSERT INTO images (image, caption, portfolio_id) VALUES (%(image)s, %(caption)s, %(portfolio_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    #Select all works of a user with portfolio description also
    @classmethod
    def get_user_images(cls, data):
        query = 'SELECT images.image AS image FROM users JOIN portfolios ON users.id = portfolios.user_id JOIN images ON portfolios.id = images.portfolio_id WHERE users.id = %(user_id)s AND portfolios.id = %(portfolio_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        images= []
        if results:
            for image in results:
                images.append(image)
            return images
        return images
    
    @classmethod
    def get_image_by_id(cls, data):
        query = 'SELECT images.id as id, images.image as image, images.caption as caption, portfolios.user_id as user_id FROM images LEFT JOIN portfolios on images.portfolio_id = portfolios.id WHERE images.id = %(image_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def edit_image(cls, data):
        query = "UPDATE images SET caption = %(caption)s WHERE images.id = %(image_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_image(cls,data):
        query = "DELETE FROM images WHERE id = %(image_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_3_last_images(cls):
        query = 'SELECT images.*, users.first_name, users.last_name,users.status, users.id AS user_id FROM images JOIN portfolios ON images.portfolio_id = portfolios.id JOIN users ON portfolios.user_id = users.id WHERE users.status = "artist" ORDER BY created_at  DESC LIMIT 3 ;'
        results = connectToMySQL(cls.db_name).query_db(query)
        images = []
        if results:
            for image in results:
                images.append(image)
            return images
        return images
    
    @staticmethod
    def validate_image(data):
        is_valid = True
        if len(data['caption'])< 2:
            flash('Description must be more than 2 characters', 'imageCaption')
            is_valid = False
        else:
            flash('Successfully updated', 'success')
        return is_valid
    
