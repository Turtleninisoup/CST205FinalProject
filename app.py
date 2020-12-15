# CST 205
# Cathy Hsu, Christiana Libhart, Jaclyn Libhart, Deborah Meda, Charlie Nguyen
# This file, is the the main file for our CST 205 final project.
#
# Citation
# https://stackoverflow.com/questions/21217475/get-selected-text-from-a-form-using-wtforms-selectfield
# https://hackersandslackers.com/flask-wtforms-forms/
# https://stackoverflow.com/questions/44055471/how-can-i-add-a-flask-wtforms-selectfield-to-my-html
# https://datatofish.com/delete-file-folder-python/
# https://www.geeksforgeeks.org/python-opencv-cv2-imwrite-method/
# https://discord.com/channels/778798502020513813/778798503408304141/788202133630877717
#https://discord.com/channels/778798502020513813/778798503408304141/788202159614853150

from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from webscrape_recipe_file import website_recipe_info
from pprint import pprint
import urllib.request       # for saving images
from PIL import Image
import cv2
import webscrape                        # webscrape



app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

# Class is used to save the users search term and their image format.
class RecipeSearchTerm(FlaskForm):
    search_term = StringField(
        'Search Term', 
        validators=[DataRequired()]
    )

    image_format = SelectField("Choose an option", choices=[("none", "None"), ("grayscale", "Grayscale"), ("negative", "Negative"), ("sephia", "Sephia"), ("thumbnail", "Thumbnail"), ("winter", "Winter")])

# Instance Variables
recipes = []
matched_recipes = []
image_filter = "none"

# run webscrape file
# We arent running this function at the moment, as all our data is already pulled
# Charlie created
def run_webscrape():
    webscrape.webscrape_function()

# split search term into separate words and convert words to lower case
# Cathy created
def store_search_term(token):
    search_term = token.lower().split()
    return search_term

# clean webscrape data
# Cathy created
def preprocess(): 
    for recipe in website_recipe_info: 
        recipes.append({})
        recipes[-1]['title'] = recipe['title']
        recipes[-1]['recipe_url'] = recipe['recipe_url']
        # split tag into separate words and convert words to lower case 
        recipes[-1]['tags'] = recipe['tags'].lower().split()
        recipes[-1]['image_url'] = recipe['image_url']

# This functions searches for recipes that matches a search term
# Cathy created
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

# This function applies a gray scale filter on the specified image.
# Christiana and Jaclyn created
def apply_grayscale(image_name, recipe_title): 
    im = Image.open(image_name)
    grayscale_list = [ ( (a[0]+a[1]+a[2])//3, ) * 3
                  for a in im.getdata() ]
    im.putdata(grayscale_list)
    im.save("static/images/grayscale/" + recipe_title + ".jpg")

# This function applies a negative filter on the specified image.
# Christiana and Jaclyn created
def apply_negative(image_name, recipe_title): 
    im = Image.open(image_name)
    negative_list = [(255 - p[0], 255 - p[1], 255 - p[2]) for p in im.getdata()]
    im.putdata(negative_list)
    im.save("static/images/negative/" + recipe_title + ".jpg")

# This function applies a thumbnail scale on the specified image.
# The image will show a canvas color
# Christiana and Jaclyn created
def apply_thumbnail(image_name, recipe_title):
    source = Image.open(image_name)
    w,h = source.width, source.height
    target = Image.new('RGB', (w, h), 'rosybrown')

    target_x = 0
    for source_x in range(0, source.width, 2):
        target_y = 0
        for source_y in range(0, source.height, 2):
            pixel = source.getpixel((source_x, source_y))
            target.putpixel((target_x, target_y), pixel)
            target_y += 1
        target_x += 1
    target.save("static/images/thumbnail/" + recipe_title + ".jpg")

# This function applies a sephia filter on the specified image.
# Christiana and Jaclyn created
def apply_sephia(image_name, recipe_title): 
    im = Image.open(image_name)
    sepia_list = [(255 + pixel[0], pixel[1], pixel[2])
                    for pixel in im.getdata()]
    im.putdata(sepia_list)
    im.save("static/images/sephia/" + recipe_title + ".jpg")

# This function applies a winter filter (color map) on the specified image.
# Christiana and Jaclyn created
def apply_winter(image_name, recipe_title): 
    image_winter = cv2.imread(image_name,cv2.IMREAD_GRAYSCALE)
    image_remap = cv2.applyColorMap(image_winter, cv2.COLORMAP_WINTER)
    cv2.imwrite("static/images/winter/" + recipe_title + ".jpg", image_remap)

# This function encapsulates all the filters into one wrapper function for ease of use
# Cathy created
def apply_filter(image_filter):
    # Index to index into matched recipes :3c
    i = 0
    pprint(matched_recipes)
    
    for recipe in matched_recipes:
        if image_filter == "grayscale":
            matched_recipes[i]["image_url"] = "static/images/grayscale/" + recipe['title'] + ".jpg"
        
        if image_filter == "negative":
            matched_recipes[i]["image_url"] = "static/images/negative/" + recipe['title'] + ".jpg"

        if image_filter == "sephia":
            matched_recipes[i]["image_url"] = "static/images/sephia/" + recipe['title'] + ".jpg"

        if image_filter == "winter":
            matched_recipes[i]["image_url"] = "static/images/winter/" + recipe['title'] + ".jpg"

        if image_filter == "thumbnail":
            matched_recipes[i]["image_url"] = "static/images/thumbnail/" + recipe['title'] + ".jpg"

        i += 1


# this will be run once to save all the images in our directory the filter images
# Cathy created
def create_filter_images(): 
    index = 0 
    for recipe in recipes:
        print("inside of matched_recipes loop")
        #print(recipe)
        image_name = "static/images/" + recipe["title"] + ".jpg"
        current_image_url = recipe["image_url"]
        # retrieve the image and save it
        urllib.request.urlretrieve(current_image_url, image_name)
        im = Image.open(image_name)
        # filters
        apply_grayscale(image_name, recipe["title"])
        apply_negative(image_name, recipe["title"])
        apply_thumbnail(image_name, recipe['title'])
        apply_sephia(image_name, recipe['title'])
        apply_winter(image_name, recipe['title'])
        index += 1
        
# Home route or landing page
# Cathy created
@app.route('/', methods=('GET', 'POST'))
def index():
    preprocess()
    form = RecipeSearchTerm()
    # when the user hits submit we will grab out the information we need
    if form.validate_on_submit():
        search_term = store_search_term(form.search_term.data)
        image_filter = form.image_format.data
        print(image_filter)
        search_for_recipe_matches(search_term)
        # create_filter_images()   
        apply_filter(image_filter)
        return redirect('/result')
    return render_template('index.html', form=form)

# result route
# Debbie created
@app.route('/result')
def vp():
    pprint(matched_recipes)
    return render_template('result.html', matched_recipes=matched_recipes)