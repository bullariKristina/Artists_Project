from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
from flask import flash
 
class Job:
    db_name = 'artistProject'
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.salary = data['salary']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_job(cls, data):
        query = "INSERT INTO jobs (title, description, salary, user_id) VALUES ( %(title)s, %(description)s, %(salary)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    #List of users who applied for a given job
    @classmethod
    def get_users_who_applied(cls, data):
        query = "SELECT applications.user_id as id FROM applications WHERE job_id = %(job_id)s;"
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
        query = 'SELECT jobs.id as id, jobs.title as title, jobs.description as description, jobs.salary as salary, jobs.user_id as user_id, COUNT(applications.id) as applications FROM jobs LEFT JOIN users on jobs.user_id = users.id LEFT JOIN applications on applications.job_id = applications.id GROUP BY applications.id;'
        results = connectToMySQL(cls.db_name).query_db(query)
        jobs= []
        if results:
            for job in results:
                jobs.append(job)
            return jobs
        return jobs
    
    @classmethod
    def get_jobs(cls):
        query = 'SELECT jobs.id as id, jobs.title as title, jobs.description as description, jobs.salary as salary, jobs.user_id as user_id, COUNT(applications.id) as applications FROM jobs LEFT JOIN users on jobs.user_id = users.id LEFT JOIN applications on applications.job_id = jobs.id GROUP BY jobs.id, jobs.title, jobs.description, jobs.salary, jobs.user_id;'
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
    

    
    @classmethod
    def delete_job(cls, data):
        query = "DELETE FROM jobs WHERE id = %(job_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    #Needed when you delete a user who has jobs published
    @classmethod
    def delete_all_user_jobs(cls, data):
        query = "DELETE FROM jobs WHERE user_id = %(user_id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def apply(cls, data):
        query = "INSERT INTO applications (user_id, job_id) VALUES ( %(user_id)s, %(job_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_4_last_jobs(cls):
        query = 'SELECT jobs.*, users.first_name, users.last_name FROM jobs JOIN users ON jobs.user_id = users.id ORDER BY created_at DESC LIMIT 4'
        results = connectToMySQL(cls.db_name).query_db(query)
        jobs = []
        if results:
            for job in results:
                jobs.append(job)
            return jobs
        return jobs
    
    @staticmethod
    def validate_job(data):
        is_valid = True
        # test whether a field matches the pattern
        if len(data['title'])< 2:
            flash('Title must be more than 2 characters', 'jobTitle')
            is_valid = False
        if len(data['description'])< 2:
            flash('Description must be more than 2 characters', 'jobDescription')
            is_valid = False
        if len(data['salary'])< 1:
            flash('Salary is required', 'jobSalary')
            is_valid= False
        else:
            flash('Job successfully posted!', 'success')
        return is_valid


    
