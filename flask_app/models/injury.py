from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, athlete, injury

class Injury:
    db='myathlete_schema'
    def __init__(self,data):
        self.id = data['id']
        self.sport = data['sport']
        self.date_injured = data['date_injured']
        self.body_part = data['body_part']
        self.subjective = data['subjective']
        self.objective = data['objective']
        self.assessment = data['assessment']
        self.plan = data['plan']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.athlete_id = data['athlete_id']
        self.user_id = data['user_id']
        self.athlete = None

#create
    @classmethod 
    def save(cls,data):
        query = '''INSERT INTO injuries (sport, date_injured, body_part, subjective, 
        objective, assessment, plan, athlete_id, user_id) 
        VALUES (%(sport)s, %(date_injured)s, %(body_part)s, %(subjective)s, 
        %(objective)s, %(assessment)s, %(plan)s, %(athlete_id)s, %(user_id)s);'''
        return connectToMySQL(cls.db).query_db(query,data)

#Read
    @classmethod 
    def get_injuries(cls):
        query = "SELECT * FROM injuries LEFT JOIN users ON user_id = users.id;"
        results=connectToMySQL(cls.db).query_db(query)
        injuries = []
        for row in results:
            injury = cls(row)
            user_data = {
                'id':row['users.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at'],            
            }
            injury.user = user.User(user_data)
            injuries.append(injury)
        return injuries

    @classmethod 
    def get_injured_athletes(cls):
        query = "SELECT * FROM injuries LEFT JOIN athletes ON athlete_id = athletes.id;"
        results=connectToMySQL(cls.db).query_db(query)
        injuries = []
        for row in results:
            injury = cls(row)
            athlete_data = {
                'id':row['athletes.id'],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'dob':row['dob'],
                'sport':row['sport'],
                'created_at':row['athletes.created_at'],
                'updated_at':row['athletes.updated_at'],
                'user_id': row['athletes.user_id']           
            }
            injury.athlete = athlete.Athlete(athlete_data)
            injuries.append(injury)
            print('get injured athletes from model',injuries)
        return injuries

#Update
    @classmethod
    def update(cls,data):
        query='''UPDATE injuries SET sport=%(sport)s, date_injured=%(date_injured)s, subjective=%(subjective)s, 
        objective=%(objective)s, assessment=%(assessment)s, plan=%(plan)s WHERE id=%(id)s;'''
        return connectToMySQL(cls.db).query_db(query,data)

#Delete
    @classmethod
    def delete_injury(cls,id):
        data = {
            'id':id
        }
        query = "DELETE FROM injury WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

#Validate
    
    @staticmethod
    def validate_injury(injury):
        is_valid = True
        if len(injury['body_part']) < 1:
            is_valid = False
            flash('Must enter a body part', 'injury')
        if len(injury['subjective']) < 1:
            flash('Must enter subjective information', 'injury')
            is_valid = False
        if len(injury['objective']) < 1:
            flash('Must enter objective information', 'injury')
            is_valid = False
        if len(injury['assessment']) < 1:
            flash('Must enter an assessment', 'injury')
            is_valid = False
        if len(injury['plan']) < 1:
            flash('Must enter a plan', 'injury')
            is_valid = False
        return is_valid

