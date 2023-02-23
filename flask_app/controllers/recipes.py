from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe

@app.route('/create_one_recipe')
def create_one_recipe():
    return render_template('create_recipe_page.html')

@app.route('/save_one_recipe', methods = ['POST'])
def save_one_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_one_recipe')
    form_data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'cooked': request.form['cooked'],
        'under_30': request.form['under_30']
    }
    Recipe.save_recipe(form_data)
    return redirect('/user_page')
