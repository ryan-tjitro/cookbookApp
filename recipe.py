class Recipe:
    def __init__(self, title, cook_time):
        self.title = title
        self.cook_time = cook_time
        # self.yield
        # self.ingredients
        # self.instructions
        # self.images

    def __str__(self):
        return "Title: " + self.title + "\nCook time: " + str(self.cook_time)
