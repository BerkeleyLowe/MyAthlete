from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, athlete, injury
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods=['POST'])
def register():
    if not user.User.validate_register(request.form):
        return redirect('/')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
        #generate_password_hash() is the standard term used to generate a password hash
    }
    userId = user.User.save(data)
    session['user_id'] = userId
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    userId = session['user_id']
    new_user=user.User.getById(userId)
    injured_athletes = injury.Injury.get_injured_athletes()
    print(injured_athletes, 'from controller')
    return render_template("dashboard.html", user=new_user, injured_athletes = injured_athletes)

@app.route('/user/login', methods = ['POST'])
def login():
    
    if not user.User.validate_login(request.form):
        return redirect('/')
    new_user = user.User.getByEmail(request.form)
    if not new_user:
        return redirect('/')
    if not bcrypt.check_password_hash(new_user.password, request.form['password']):
        return redirect('/')
    userId = user.User.getByEmail(request.form)
    session['user_id'] = new_user.id 
    return redirect('/dashboard')

@app.route('/user/account')
def account():
    if 'user_id' not in session:
        return redirect('/logout')
    userId = session['user_id']
    new_user=user.User.getById(userId)
    return render_template("dashboard.html", user=new_user, injuries= injury.Injury.get_injuries())
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')