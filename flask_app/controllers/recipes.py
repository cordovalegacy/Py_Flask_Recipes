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
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    Recipe.save_recipe(form_data)
    return redirect('/user_page')

@app.route('/delete_one_recipe/<int:id>')
def delete_one_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/user_page')

@app.route('/edit_one_recipe/<int:id>')
def edit_one_recipe(id):
    data={
        'id':id
    }
    return render_template('edit_recipe.html', one_ninja = Recipe.edit_one_recipe_view(data))