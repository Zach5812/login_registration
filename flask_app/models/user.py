# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DATABASE = "login"

class User:
    
    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    

    @classmethod
    def find_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        if len(result) > 0:
            user = User(result[0])
            return user
        else:
            return False
        
    @staticmethod
    def validate_user(user):
        is_valid = True
        if User.find_by_email(user['email']):
            is_valid = False
            flash("you have already registered!!!!")
        if len(user['first_name']) < 2:
            is_valid = False
            flash("first name must be at least 2 chars")
        if len(user['last_name']) < 4:
            is_valid = False
            flash("last name must be at least 4 chars")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("passwords must match")
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid



