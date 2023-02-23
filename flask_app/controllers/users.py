from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('registration.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate(request.form):
        return redirect('/')
    form_data = {
        'first_name': request.form['first_name'], 
        'last_name': request.form['last_name'], 
        'email': request.form['email'], 
        'password': bcrypt.generate_password_hash(request.form['password']) 
    }
    id = User.save_registration(form_data)
    session['user_id'] = id
    return redirect('/user_page')

@app.route('/login', methods = ['POST'])
def login():
    logged_user = User.get_one_user_by_email(request.form)
    if not logged_user:
        flash("Invalid Email Address", 'Login')
        return redirect('/login_page')
    if not bcrypt.check_password_hash(logged_user.password, request.form['password']):
        return redirect('/')
    session['user_id'] = logged_user.id
    return redirect('/user_page')

@app.route('/user_page')
def user_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('user_page.html', user = User.get_one_user_by_id(data), all_recipes = Recipe.get_all_recipes())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')