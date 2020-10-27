import pymysql
from recipe import Recipe

conn = pymysql.connect(
    db='cookbook',
    user='root',
    passwd='C00kb00kApp',
    host='localhost')
c = conn.cursor()

def insert_recipe(recipe):
    potential_recipe = fetch_recipe(recipe.get_title())
    if potential_recipe is None:
        values = [recipe.get_title(), str(recipe.get_cook_time()), str(recipe.get_recipe_yield()), "ingredients", "instructions", recipe.get_original_url()]
        formatted = [wrap_with_quotes(val) for val in values]
        insert_query = "INSERT INTO recipes VALUES (" + ",".join(formatted) + ");"
        c.execute(insert_query)
        conn.commit()
    else:
        print("Recipe with this name already exists!")

def get_all_recipes():
    c.execute("SELECT * FROM recipes;")
    return [Recipe(r[0], r[1], r[2], r[3], r[4], r[5]) for r in c.fetchall()]

def fetch_recipe(recipe_title):
    existence_query = "SELECT * FROM recipes WHERE title = " + wrap_with_quotes(recipe_title) + ";"
    c.execute(existence_query)
    results = [Recipe(r[0], r[1], r[2], r[3], r[4], r[5]) for r in c.fetchall()]
    if len(results) == 0:
        return None
    else:
        return results[0]

def wrap_with_quotes(value):
    return "'" + value + "'"
