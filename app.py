
from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from webscrape_recipe_file import website_recipe_info
from pprint import pprint
import urllib.request       # for saving images
from PIL import Image
import os
import shutil

# Citation
# https://stackoverflow.com/questions/21217475/get-selected-text-from-a-form-using-wtforms-selectfield

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class RecipeSearchTerm(FlaskForm):
    search_term = StringField(
        'Search Term', 
        validators=[DataRequired()]
    )

    image_format = SelectField("Choose an option", choices=[("none", "None"), ("grayscale", "Grayscale"), ("negative", "Negative"), ("sephia", "Sephia")])

recipes = []
matched_recipes = []
image_filter = "none"

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

def apply_filter(image_filter):
    # Deleting old files
    shutil.rmtree(r"static/images/filter")
    os.mkdir(r"static/images/filter")

    # Index to index into matched recipes :3c
    i = 0

    # This will save our images to our directory
    for recipe in matched_recipes:
        print("inside of matched_recipes loop")
        #print(recipe)
        image_name = "static/images/" + recipe["title"] + ".jpg"
        current_image_url = recipe["image_url"]
        print(current_image_url)
        # retreieve the image and save it
        urllib.request.urlretrieve(current_image_url, image_name)
        im = Image.open(image_name)
        print("Line 76" + image_filter)
        if image_filter == "grayscale":
            grayscale_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                  for a in im.getdata() ]
            im.putdata(grayscale_list)
            im.save("static/images/filter/" + recipe["title"] + ".jpg")
            matched_recipes[i]["image_url"] = "static/images/filter/" + recipe["title"] + ".jpg"
        i += 1

@app.route('/', methods=('GET', 'POST'))
def index():
    preprocess()
    form = RecipeSearchTerm()
    if form.validate_on_submit():
        search_term = store_search_term(form.search_term.data)
        image_filter = form.image_format.data
        print(image_filter)
        search_for_recipe_matches(search_term)
        pprint(matched_recipes)

        apply_filter(image_filter)
        return redirect('/result')
    return render_template('index.html', form=form)

@app.route('/result')
def vp():
    return render_template('result.html', matched_recipes=matched_recipes)