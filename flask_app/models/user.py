from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one_user_by_id(cls, data):
        query = "SELECT * FROM users_table WHERE id=%(id)s"
        result = connectToMySQL('recipes').query_db(query, data)
        if not result:
            return False
        print(result[0])
        return cls(result[0])

    @classmethod
    def get_one_user_by_email(cls, data):
        query = "SELECT * FROM users_table WHERE email=%(email)s"
        result = connectToMySQL('recipes').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save_registration(cls, form_data):
        query = """
                INSERT INTO users_table (first_name, last_name, email, password, created_at, updated_at)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
                ;"""
        return connectToMySQL('recipes').query_db(query, form_data)
    
    @staticmethod
    def validate(form_data):
        is_valid = True
        query = """
                SELECT * FROM users_table 
                WHERE email = %(email)s
                ;"""
        results = connectToMySQL('recipes').query_db(query, form_data)
        if len(results) >=1:
            flash("Email is taken, enter a different one", 'Register')
            is_valid = False
        if len(form_data['first_name']) < 2:
            flash("First Name must be at least 2 characters", 'Register')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last Name must be at least 2 characters", 'Register')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']):
            flash("Please register with a valid email address", 'Register')
            is_valid = False
        if len(form_data['password']) < 7:
            flash("Password must be at least 7 characters", 'Register')
            is_valid = False
        if form_data['password'] != form_data['confirm']:
            flash("Passwords must match", 'Register')
            is_valid = False
        return is_valid


