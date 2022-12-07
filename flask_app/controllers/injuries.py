from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import athlete, user, injury
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/injury/new')
def new_injury():
    userId = session['user_id']
    new_user=user.User.getById(userId)
    # athleteId = session['athlete_id']
    # new_athlete = athlete.Athlete.getAthleteById(athleteId)
    return render_template('add_injury.html', user=new_user, athletes= athlete.Athlete.get_athletes())

@app.route('/injury/create', methods=['POST'])
def create_injury():
    if not injury.Injury.validate_injury(request.form):
        return redirect('/injury/new')
    injury.Injury.save(request.form)
    return redirect('/dashboard')

@app.route('/injury/<int:id>')
def show_injury(id):
    userId = session['user_id']
    new_user=user.User.getById(userId)
    return render_template('injury.html', user=new_user, injury=injury.Injury.get_injured_athletes(id))

#this is the GET request to be able to edit the injury info
@app.route('/injury/edit/<int:id>')
def edit_injury(id):
    data= {
        'id':id
    }
    userId = session['user_id']
    new_user=user.User.getById(userId)
    return render_template('edit_injury.html',user=new_user, injury=injury.Injury.get_one_injury(id))

#this is the route to submit that change to the database, so our POST method
@app.route('/injury/update', methods=['POST'])
def update_injury():
    if not injury.Injury.validate_injury(request.form):
        return redirect(f"/injury/edit/{request.form['id']}")
    injury.Injury.update(request.form)
    return redirect(f"/injury/{request.form['id']}")

@app.route('/delete/<int:id>')
def delete_injury(id):
    injury.Injury.delete_injury(id)
    return redirect('/dashboard')