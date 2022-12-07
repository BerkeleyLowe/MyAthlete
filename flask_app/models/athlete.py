from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, injury, athlete

class Athlete:
    db='myathlete_schema'
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dob = data['dob']
        self.sport = data['sport']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.injuries = []

    # def __repr__(self) -> str:
    #     return f'Athlete instance ; {self.first_name},{self.user_id},{self.id},{self.injuries}'

#create
    @classmethod 
    def save(cls,data):
        query = '''INSERT INTO athletes (first_name, last_name, dob, sport, user_id) 
        VALUES (%(first_name)s, %(last_name)s, %(dob)s, %(sport)s, %(user_id)s);'''
        return connectToMySQL(cls.db).query_db(query,data)

#Read
    @classmethod 
    def get_athletes(cls):
        query = "SELECT * FROM athletes LEFT JOIN users ON user_id = users.id;"
        results=connectToMySQL(cls.db).query_db(query)
        athletes = []
        for row in results:
            athlete = cls(row)
            user_data = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],            
            }
            athlete.user = user.User(user_data)
            athletes.append(athlete)
        return athletes

    @classmethod
    def getAthleteById(cls,id):
        data = {
            'id':id
        }
        query='SELECT * FROM athletes WHERE id = %(id)s;'
        results =  connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])



#Validate
    
    @staticmethod
    def validate_athlete(athlete):
        is_valid = True
        if len(athlete['first_name']) < 1:
            is_valid = False
            flash('Must enter a first name', 'athlete')
        if len(athlete['last_name']) < 1:
            flash('Must enter a last name', 'athlete')
            is_valid = False
        if len(athlete['sport']) < 1:
            flash('Must enter current sport', 'athlete')
            is_valid = False
        return is_valid
