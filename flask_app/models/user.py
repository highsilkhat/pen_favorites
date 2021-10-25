from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash
import re

from flask_app.models import pen

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at =  data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls, data):

        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        new_user_id = connectToMySQL('pens_schema').query_db(query, data)

        return new_user_id

    @classmethod
    def get_one_user_by_email(cls, data):

        query = 'SELECT * FROM users WHERE email = %(email)s;'

        results = connectToMySQL('pens_schema').query_db(query, data)

        users = []

        for user in results:
            users.append (User (user))
        print (users)
        return users

    @staticmethod
    def validate_user(data):

        is_valid= True

        if len(data['first_name']) < 3 or len(data['first_name']) > 45:
            is_valid = False
            flash('First name must be between 3 and 45 characters')
    
        if len(data['last_name']) < 3 or len(data['last_name']) > 45:
            is_valid = False
            flash('Last name must be between 3 and 45 characters')

        if len(User.get_one_user_by_email({'email' :data['email']})) > 0:
            is_valid = False
            flash ('Email already registered')

        if len(data['email']) > 45:
            is_valid = False
            flash('Email address is too long. Must be fewer than 255 characters')

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address")
            is_valid = False

        if len(data['newPassword']) < 8 or len(data['newPassword']) > 60:
            is_valid = False
            flash("Please create a password of at least 8 characters")
        
        if data['confirmPassword'] != data['newPassword']:
            is_valid = False
            flash("Your passwords do not match")

        return is_valid