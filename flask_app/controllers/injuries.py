from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import athlete, user, injury
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/injury/new')
def new_injury():
    userId = session['user_id']
    new_user=user.User.getById(userId)
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
    print('show me the injury', injury)
    return render_template('injury.html', user=new_user, injury=injury.Injury.get_one_injury(id))

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
@app.route('/injury/<int:injury_id>/update', methods=['POST'])
def update_injury(injury_id):
    # if not injury.Injury.validate_injury(request.form):
    #     return redirect(f"/injury/edit/{request.form['athlete.injury.id']}")
    data = {
        "id": injury_id,
        "sport": request.form['sport'],
        "date_injured" : request.form['date_injured'],
        "body_part" : request.form['body_part'],
        "subjective" : request.form['subjective'],
        "objective" : request.form['objective'],
        "assessment" : request.form['assessment'],
        "plan" : request.form['plan'],
        "athlete_id" : request.form['athlete_id'],
        "user_id" : session['user_id']
    }
    # for key, value in data.items():
    #     print(key,"\t\t",value)
    injury.Injury.update(data)
    return redirect(f'/injury/{injury_id}')

@app.route('/delete/<int:injury_id>')
def delete_injury(injury_id):
    injury.Injury.delete_injury(injury_id)
    return redirect('/dashboard')