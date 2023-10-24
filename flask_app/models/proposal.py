from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Proposal:
    db_name = 'project_artist_it'
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
    
    @classmethod
    def get_proposals(cls):
        try:
            query = 'SELECT * FROM proposals;'
            results = connectToMySQL(cls.db_name).query_db(query)
            if results:
                return results
            else:
                return []
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []
        
    @classmethod
    def get_proposal_by_id(cls, data):
        query = 'SELECT * FROM proposals WHERE id= %(proposal_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    @classmethod
    def get_users_for_proposal(cls, data):
        query = 'SELECT * FROM users LEFT JOIN proposals ON users.developer = proposals.skill1 AND users.language = proposals.skill2  WHERE proposals.id = %(proposal_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        users= []
        if results:
            for user in results:
                users.append(user)
            return users
        return users
    

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