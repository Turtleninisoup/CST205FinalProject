from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from webscrape_recipe_file import website_recipe_info
from pprint import pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class RecipeSearchTerm(FlaskForm):
    search_term = StringField(
        'Search Term', 
        validators=[DataRequired()]
    )

recipes = []
matched_recipes = []

# split search term into separate words and convert words to lower case
def store_search_term(token):
    search_term = token.lower().split()
    return search_term

# clean webscrape data
def preprocess(): 
    for recipe in website_recipe_info: 
        recipes.append({})
        recipes[-1]['title'] = recipe['title']
        recipes[-1]['recipe_url'] = recipe['recipe_url']
        # split tag into separate words and convert words to lower case 
        recipes[-1]['tags'] = recipe['tags'].lower().split()
        recipes[-1]['image_url'] = recipe['image_url']

def search_for_recipe_matches(search_term): 
    # empty array so recipes that matched previous search term aren't included
    matched_recipes.clear()
    # used to check if a recipe has already been added into matched_recipes
    already_matched_recipe_titles = []

    # for every word in the search_term, go through each recipe's tags and check if the word matches any word in the 
    # tag. If there is a match and the recipe has not already been added, add it to matched_recipes
    for word in search_term: 
        for recipe in recipes: 
            for tag in recipe['tags']: 
                if (tag == word and recipe['title'] not in already_matched_recipe_titles):
                    matched_recipes.append({})
                    already_matched_recipe_titles.append(recipe['title'])
                    matched_recipes[-1]['title'] = recipe['title']
                    matched_recipes[-1]['recipe_url'] = recipe['recipe_url']
                    matched_recipes[-1]['tags'] = recipe['tags']
                    matched_recipes[-1]['image_url'] = recipe['image_url']

@app.route('/', methods=('GET', 'POST'))
def index():
    preprocess()
    form = RecipeSearchTerm()
    if form.validate_on_submit():
        search_term = store_search_term(form.search_term.data)
        search_for_recipe_matches(search_term)
        pprint(matched_recipes)
        return redirect('/result')
    return render_template('index.html', form=form)

@app.route('/result')
def vp():
    return render_template('result.html', matched_recipes=matched_recipes)