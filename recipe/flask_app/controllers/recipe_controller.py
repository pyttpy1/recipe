from flask_app import app, render_template, redirect, request, session
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

# display all recipes
@app.get('/recipes')
def all_recipes():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': session['user_id']
    }
    user = User.find_by_id(data)
    recipes = Recipe.find_all()
    return render_template('all_recipes.html', user = user, recipes = recipes)

# display form to create recipe
@app.get('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    return render_template('new_recipe.html')

# process form and create recipe
@app.post('/recipes')
def create_recipe():
    if not Recipe.validate_recipe_form(request.form):
        return redirect('/recipes/new')
    Recipe.save(request.form)
    return redirect('/recipes')

# display one recipe
@app.get('/recipes/<int:recipe_id>')
def one_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.find_by_id_with_creator(data)
    return render_template('one_recipe.html', recipe = recipe)

# display form to edit recipe
@app.get('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    recipe = Recipe.find_by_id_with_creator(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.post('/recipes/<int:recipe_id>/update')
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')
    Recipe.find_by_id_and_update(request.form)
    return redirect(f'/recipes/{recipe_id}')

@app.get('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/users/login_reg')
    data = {
        'id': recipe_id
    }
    Recipe.find_by_id_and_delete(data)
    return redirect('/recipes')