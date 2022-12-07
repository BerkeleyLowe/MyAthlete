from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import athlete, user, injury
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/roster')
def roster():
    userId = session['user_id']
    new_user=user.User.getById(userId)
    return render_template("roster.html", user=new_user, athletes= athlete.Athlete.get_athletes(), injury= injury.Injury.get_injuries())

@app.route('/athlete/new')
def new_athlete():
    userId = session['user_id']
    new_user=user.User.getById(userId)
    return render_template('add_athlete.html', user=new_user)

@app.route('/athlete/create', methods=['POST'])
def create_athlete():
    if not athlete.Athlete.validate_athlete(request.form):
        return redirect('/athlete/new')
    athlete.Athlete.save(request.form)
    return redirect('/dashboard')


