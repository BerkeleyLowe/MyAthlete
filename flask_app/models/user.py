from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#format for email, lines 4 and 5 import regex
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class User:
    db='myathlete_schema'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    def __repr__(self) -> str:
        return f'User instance ; {self.first_name},{self.id}'

#Create

    @classmethod 
    def save(cls,data):
        query = '''INSERT INTO users (first_name, last_name, email, password) 
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);'''
        
        return connectToMySQL(cls.db).query_db(query,data)

#Read
    @classmethod
    def getById(cls,id):
        data = {
            'id':id
        }
        query='SELECT * FROM users WHERE id = %(id)s;'
        results =  connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def getByEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    #Validate
    @staticmethod
    def validate_register(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        #run the query to make sure there are no duplicates
        results = connectToMySQL(User.db).query_db(query,user)
        #cant pass in cls.db because we are doing a static method and not a class method
        if len(results) >= 1:
            flash('email already taken...find another', 'register')
            is_valid = False 
        if len(user['first_name']) < 3:
            flash("First name must be a least 3 characters", 'register')
            is_valid = False 
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format', 'register')
            #must import regex
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters','register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", "register")
            is_valid = False
        return is_valid 

    @staticmethod
    def validate_login(user):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        is_valid = True
        if not results:
            flash("invalid email or password", 'login')
            is_valid = False
        elif not bcrypt.check_password_hash(User(results[0]).password, user['password']):
            flash('invalid email or password', 'login')
            is_valid = False
        return is_valid