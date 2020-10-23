from recipe_scrapers import scrape_me
import recipe
import sys

url = str(sys.argv[1])

# give the url as a string, it can be url from any site listed below
scraper = scrape_me(url)

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
# scraper = scrape_me('https://www.feastingathome.com/tomato-risotto/', wild_mode=True)

scraper.title()
scraper.total_time()
scraper.yields()
# print(scraper.ingredients())
scraper.instructions()
scraper.image()
scraper.host()
scraper.links()


new_recipe = recipe.Recipe(scraper.title(), scraper.total_time())
print(new_recipe)
