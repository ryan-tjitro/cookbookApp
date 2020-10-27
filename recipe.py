class Recipe:
    def __init__(self, title, cook_time, recipe_yield, ingredients, instructions, original_url):
        self.title = title
        self.cook_time = cook_time
        self.recipe_yield = recipe_yield
        self.ingredients = ingredients
        self.instructions = instructions
        self.original_url = original_url
        # self.images

    def __str__(self):
        result_string = "Title: " + self.title
        result_string += "\nCook Time: " + str(self.cook_time)
        result_string += "\nYields: " + self.recipe_yield
        result_string += "\nIngredients: " + self.ingredients
        result_string += "\nInstructions: " + self.instructions
        result_string += "\nLink: " + self.original_url
        return result_string

    def get_title(self):
        return self.title

    def get_cook_time(self):
        return self.cook_time

    def get_recipe_yield(self):
        return self.recipe_yield

    def get_ingredients(self):
        return self.ingredients

    def get_instructions(self):
        return self.instructions

    def get_original_url(self):
        return self.original_url
