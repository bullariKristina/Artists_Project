from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Job:
    db_name = 'first_project'
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['title']
        self.description = data['description']
        self.salary = data['salary']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_job(cls, data):
        query = "INSERT INTO jobs (title, instructions, salary, user_id) VALUES ( %(title)s, %(description)s,%(salary)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    # @classmethod
    # def unlike(cls, data):
    #     query = "DELETE FROM likes WHERE user_id = %(user_id)s AND recipe_id = %(recipe_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    
    
    #List of users who applied for a given job
    @classmethod
    def get_users_who_applied(cls, data):
        query = "SELECT applications.user_id as id FROM applicatins WHERE job_id = %(job_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        applications= []
        if results:
            for application in results:
                applications.append(application['id'])
            return applications
        return applications
    
    #List of all jobs we have 
    @classmethod
    def get_all_jobs(cls):
        query = 'SELECT jobs.id as id, jobs.title as title, recipes.salary as salary, jobs.user_id as user_id, COUNT(applications.id) as applications FROM jobs LEFT JOIN users on jobs.user_id = users.id LEFT JOIN applications on application.job_id = applications.id GROUP BY applications.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        jobs= []
        if results:
            for job in results:
                jobs.append(job)
            return jobs
        return jobs
    
    @classmethod
    def get_job_by_id(cls, data):
        query = 'SELECT * FROM jobs WHERE id= %(job_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]
        return False
    
    #List of jobs that a given user has created
    @classmethod
    def get_user_jobs(cls, data):
        query = 'SELECT * FROM jobs WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        jobs= []
        if results:
            for job in results:
                jobs.append(job)
            return jobs
        return jobs
    

    
    # @classmethod
    # def edit_recipe(cls, data):
    #     query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30 = %(under_30)s WHERE id = %(recipe_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def delete_job(cls, data):
        query = "DELETE FROM jobs WHERE id = %(job_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def delete_likes(cls, data):
    #     query = "DELETE FROM likes WHERE recipe_id = %(recipe_id)s;"
    #     return connectToMySQL(cls.db_name).query_db(query, data)
        

    #Needed when you delete a user who has jobs published
    @classmethod
    def delete_all_user_jobs(cls, data):
        query = "DELETE FROM jobs WHERE user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def apply(cls, data):
        query = "INSERT INTO applications (user_id, job_id) VALUES ( %(user_id)s, %(job_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_job(data):
        is_valid = True
        # test whether a field matches the pattern
        if len(data['title'])< 2:
            flash('Title must be more than 2 characters', 'title')
            is_valid = False
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'description')
            is_valid = False
        if len(data['salary'])< 1:
            flash('Salary is required', 'salary')
            is_valid= False
        else:
            flash('Job successfully posted!', 'success')
        return is_valid
    
