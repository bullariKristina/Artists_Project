from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Proposal:
    db_name = 'db_project'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.skill1 = data['skill1']
        self.skill2 = data['skill2']
        self.skill3 = data['skill3']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_proposal(cls, data):
        query = "INSERT INTO proposals (title, description, skill1, skill2, skill3, user_id) VALUES ( %(title)s, %(description)s, %(skill1)s, %(skill2)s, %(skill3)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @staticmethod
    def validate_proposal(data):
        is_valid = True
        if len(data['title'])<2:
            flash('Title must be more than 2 characters', 'proposalTitle')
            is_valid = False
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'proposalDescription')
            is_valid = False
        else:
            flash('Proposal successfully posted!', 'proposalSuccess')
        return is_valid