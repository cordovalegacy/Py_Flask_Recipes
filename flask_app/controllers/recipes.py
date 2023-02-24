from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models import user

@app.route('/create_one_recipe')
def create_one_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
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

@app.route('/display_one_recipe/<int:id>')
def display_one_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id'],
    }
    recipe_data = {
        'id': id
    }
    return render_template('display_recipe_page.html', one_recipe = Recipe.display_one_recipe(recipe_data), user = user.User.get_one_user_by_user_id(user_data))

@app.route('/delete_one_recipe/<int:id>')
def delete_one_recipe(id):
    data = {
        'id': id
    }
    Recipe.delete_recipe(data)
    return redirect('/user_page')

@app.route('/edit_one_recipe/<int:id>')
def edit_one_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id':id
    }
    return render_template('edit_recipe.html', one_recipe = Recipe.display_one_recipe_to_edit(data))

@app.route('/update_one_recipe/<int:id>', methods = ['POST'])
def update_one_recipe(id):
    if not Recipe.validate_recipe_edit(request.form):
        return redirect(f"/edit_one_recipe/{id}")
    form_data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'cooked': request.form['cooked'],
        'under_30': request.form['under_30']
    }
    Recipe.edit_recipe(form_data)
    return redirect("/user_page")
    