from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked = data['cooked']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posted_by = []

    @classmethod
    def save_recipe(cls, form_data):
        query = """
                INSERT INTO recipes_table
                (name, description, instructions, cooked, under_30)
                VALUES
                (%(name)s, %(description)s, %(instructions)s, %(cooked)s, %(under_30)s)
                ;"""
        return connectToMySQL('recipes').query_db(query, form_data)

    @classmethod
    def get_all_recipes(cls):
        query = """
                SELECT * FROM recipes_table
                ;"""
        return connectToMySQL('recipes').query_db(query)

    @staticmethod
    def validate_recipe(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            flash("Name of recipe must be at least 3 characters", 'Recipes')
            is_valid = False
        if len(form_data['description']) < 3:
            flash("Descirption must be at least 3 characters", 'Recipes')
            is_valid = False
        if len(form_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters", 'Recipes')
            is_valid = False
        if form_data['cooked'] == '':
            flash("Cooked field cannot be left blank", 'Recipes')
            is_valid = False
        if 'under_30' not in form_data:
            flash("Under 30 field cannot be left blank", 'Recipes')
            is_valid = False
        return is_valid