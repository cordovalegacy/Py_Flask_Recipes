from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

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
        self.user_id = data['user_id']
        self.posted_by = None

    @classmethod
    def save_recipe(cls, form_data):
        query = """
                INSERT INTO recipes_table
                (name, description, instructions, cooked, under_30, user_id)
                VALUES
                (%(name)s, %(description)s, %(instructions)s, %(cooked)s, %(under_30)s, %(user_id)s)
                ;"""
        return connectToMySQL('recipes').query_db(query, form_data)

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes_table SET name = %(name)s, description = %(description)s,  instructions = %(instructions)s, cooked = %(cooked)s, under_30 = %(under_30)s, updated_at = NOW() WHERE recipes_table.id=%(id)s"
        return connectToMySQL('dojos_and_ninjas').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes_table WHERE id=%(id)s;"
        return connectToMySQL('recipes').query_db(query, data)

#this method below is for when we have a one to many relationship, 
#where we have to get all of the many and append the 'ONE(-to-many)'(user_id in recipes_table to users_table.id) 
# by the foreign key so we can access all the information in one 'get_all' call.
    @classmethod
    def get_all_recipes_with_user(cls):
        query = """
                SELECT * FROM recipes_table
                JOIN users_table on recipes_table.user_id = users_table.id
                ;"""
        results = connectToMySQL('recipes').query_db(query)
        result = []
        for row in results:
            one_recipe = cls(row)
            one_user = {
                'id': row['users_table.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': "",
                'created_at': row['users_table.created_at'],
                'updated_at': row['users_table.updated_at']
            }
            one_recipe.posted_by = user.User(one_user)
            result.append(one_recipe)
        return result

    # @classmethod
    # def display_single_recipe(cls, data):
    #     query = """
    #             SELECT * FROM recipes_table
    #             LEFT JOIN users_and_recipes ON recipes_table.id = users_and_recipes.recipe_id
    #             LEFT JOIN users_table ON users_table.id = users_and_recipes.user_id
    #             WHERE recipes_table.id = %(id)s;
    #             ;"""
    #     results = connectToMySQL('recipes').query_db(query, data)
    #     result = cls(results[0])
    #     for row in results:
    #         data = {
    #             'id': row['users.id'],
    #             'first_name': row['first_name'],
    #             'last_name': row['last_name'],
    #             'email': row['email'],
    #             'created_at': row['created_at'],
    #             'updated_at':row['updated_at']
    #         }
    #         result.posted_by.append(user.User(data))
    #     print(result)
    #     return result

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