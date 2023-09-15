from pprint import pprint
from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model


DATABASE = 'recipe'


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        # self.instructions = data['instructions']
        self.description = data['description']
        self.under_30mins = data['under_30mins']
        self.date_made = data['date_made']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = data['creator']
    
    def __repr__(self):
        return f'<Recipe: {self.name}>'
    
    @staticmethod
    def validate_recipe_form(form):
        is_valid = True
        if len(form['name']) < 2:
            flash('Name must be at least two characters.', 'name')
            is_valid = False
        # if len(form['instructions']) < 2:
        #     flash('Instructions must be at least two characters.', 'instructions')
        #     is_valid = False
        if len(form['description']) < 10:
            flash('Description must be at least two characters.', 'description')
            is_valid = False
        if not form['under_30mins']:
            flash('Please select yes or no.', 'under_30mins')
            is_valid = False
        if not form['date_made']:
            flash('Please enter release date.', 'date_made')
            is_valid = False
        return is_valid

    # create an recipe
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, under_30mins, date_made, creator_id) VALUES (%(name)s, %(instructions)s, %(description)s, %(under_30mins)s, %(date_made)s, %(creator_id)s);'
        recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        return recipe_id

    # find all recipes (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from recipes;'
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for result in results:
            recipes.append(Recipe(result))
        return recipes

    # find all recipes with creators (no data needed)
    @classmethod
    def find_all_with_creators(cls):
        query = 'SELECT * from recipes JOIN users ON recipes.creator_id = users.id;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        recipes = []
        for result in results:
            user_data = {
                'id': result['creator_id']
            }
            creator = user_model.User.find_by_id(user_data)
            recipe_data = {
                'id': result['id'],
                'name': result['name'],
                # 'instructions': result['instructions'],
                'description': result['description'],
                'under_30mins': result['under_30mins'],
                'date_made': result['date_made'],
                'creator_id': result['creator_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'creator': creator
            }

            recipe = Recipe(recipe_data)
            recipes.append(recipe)
            
        return recipes

    # find one recipe by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from recipes WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    # find one recipe by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from recipes JOIN users ON recipes.creator_id = users.id WHERE recipes.id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user_data = {
            'id': results[0]['creator_id']
        }
        creator = user_model.User.find_by_id(user_data)
        recipe_data = {
            'id': results[0]['id'],
            'name': results[0]['name'],
            # 'instructions': results[0]['instructions'],
            'description': results[0]['description'],
            'under_30mins': results[0]['under_30mins'],
            'date_made': results[0]['date_made'],
            'creator_id': results[0]['creator_id'],
            'created_at': results[0]['created_at'],
            'updated_at': results[0]['updated_at'],
            'creator': creator
        }
        recipe = Recipe(recipe_data)
        return recipe

    # update one recipe by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, under_30mins = %(under_30mins)s, date_made = %(date_made)s, creator_id = %(creator_id)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one recipe by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True