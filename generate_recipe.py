from recipe_scrapers import scrape_me
import recipe
import sys
from sql_util import insert_recipe, get_all_recipes

url = str(sys.argv[1])

# give the url as a string, it can be url from any site listed below
scraper = scrape_me(url)

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
# scraper = scrape_me('https://www.feastingathome.com/tomato-risotto/', wild_mode=True)

new_recipe = recipe.Recipe(scraper.title(), scraper.total_time(), scraper.yields(), scraper.ingredients(), scraper.instructions(), url)
insert_recipe(new_recipe)
print()

for recipe in get_all_recipes():
    print(recipe)
    print()
