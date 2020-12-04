from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from webscrape_recipe_file import website_recipe_info
from pprint import pprint
import sys

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

def store_search_term(token):
    search_term = token.lower().split()
    return search_term
    # print("search term")
    # sys.stdout.flush()
    # print(search_term)
    # sys.stdout.flush()

def preprocess(): 
    for recipe in website_recipe_info: 
        recipes.append({})
        recipes[-1]['recipe_url'] = recipe['recipe_url']
        recipes[-1]['tags'] = recipe['tags'].lower().split()
        recipes[-1]['image_url'] = recipe['image_url']
    # for recipe in recipes: 
    #     print(recipe)
    #     sys.stdout.flush()

def search_for_recipe_matches(search_term): 
    print(search_term)
    # sys.stdout.flush()
    for word in search_term: 
        print(word)
        sys.stdout.flush()
        # for recipe in recipes: 
        #     for tag in recipes['tags']: 
        #         print(tag)
        #         sys.stdout.flush()
    print("END OF SEARCH")


@app.route('/', methods=('GET', 'POST'))
def index():
    preprocess()
    form = RecipeSearchTerm()
    if form.validate_on_submit():
        search_term = store_search_term(form.search_term.data)
        print("SEARCH TERM = ", search_term)
        sys.stdout.flush()
        search_for_recipe_matches(search_term)
        return redirect('/result')
    return render_template('index.html', form=form)

@app.route('/result')
def vp():
    return render_template('result.html')