# CST 205
# Charlie Nguyen
# 12/4/20
# need to pip install request
# need to pip install BeatifulSoup4
import requests
from bs4 import BeautifulSoup

website_url = 'http://www.tastespotting.com/'
website_page = requests.get(website_url)
website_soup = BeautifulSoup(website_page.content, 'html.parser')

# print(website_soup.prettify())
website_recipe_file = open("webscrape_recipe_file.py", "w")
website_recipe_file.write("website_recipe_info = [\n")

# used so we can figure out when the end of the list is
recipe_test = website_soup.find_all('div', 'trendspotted-item')
recipe_card_count = len(recipe_test)

for recipe_card in website_soup.find_all('div', 'trendspotted-item'):
    recipe_card_count = recipe_card_count - 1
    website_recipe_file.write("\t{\n")

    recipe_text = str(recipe_card.find('h3'))

    #print(recipe_card)
    print(recipe_text)

    # locating where the first link is at for
    # the recipe URL
    i = 30
    target_index = recipe_text.index("target")
    n = target_index - 2
    recipe_url = recipe_text[i:n]
    website_recipe_file.write("\t\t\"recipe_url\" : ")
    website_recipe_file.write("\"" + recipe_url + "\"")
    website_recipe_file.write(",\n")
    #print(recipe_url)


    # locating search words
    end_of_tags_words = recipe_text.index(" height")
    start_of_tags_Words = recipe_text.index("alt=")
    i = start_of_tags_Words + 5
    n = end_of_tags_words - 1
    snippet = recipe_text[i:]
    quote_index = snippet.index("\"")
    #print("snippet [" + snippet + "]")
    # print("location of snippet: " + snippet.index("\""))
    tag_words = snippet[:quote_index]
    website_recipe_file.write("\t\t\"tags\" : ")
    website_recipe_file.write("\"" + tag_words + "\"")
    website_recipe_file.write(",\n")
    #print(tag_words)

    # locating image location
    start_of_image = recipe_text.index("src")
    end_of_image = recipe_text.index("width")
    i = start_of_image + 5
    n = end_of_image - 2
    snippet = recipe_text[i:]
    quote_index = snippet.index("\"")
    image_url = snippet[:quote_index]
    website_recipe_file.write("\t\t\"image_url\" : ")
    website_recipe_file.write("\"" + image_url + "\"")
    website_recipe_file.write("\n")
    #print(image_url)
    #print('\n-----------------\n')
    if(recipe_card_count == 0) :
        website_recipe_file.write("\t}\n")
    else :
        website_recipe_file.write("\t},\n")

website_recipe_file.write("]")