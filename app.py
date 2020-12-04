from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from webscrape_recipe_file import website_recipe_info
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class RecipeSearchTerm(FlaskForm):
    song_title = StringField(
        'Keyword', 
        validators=[DataRequired()]
    )

playlist = []
recipes = []

def store_song(my_song):
    playlist.append(dict(
        song = my_song,
        date = datetime.today()
    ))

def preprocess(): 
    # recipe_dict = website_recipe_info.copy()
    for recipe in website_recipe_info: 
        recipes.append({})
        recipes[-1]['recipe_url'] = recipe['recipe_url']
        recipes[-1]['tags'] = recipe['tags'].lower().split()
        recipes[-1]['image_url'] = recipe['image_url']

    print("##################################")
    for recipe in recipes: 
        pprint(recipe)

@app.route('/', methods=('GET', 'POST'))
def index():
    print("HELLO")
    preprocess()
    form = RecipeSearchTerm()
    if form.validate_on_submit():
        store_song(form.song_title.data)
        return redirect('/view_playlist')
    return render_template('index.html', form=form)

@app.route('/result')
def vp():
    return render_template('vp.html', playlist=playlist)