from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instructions = models.CharField(max_length=10000, default="")
    time = models.IntegerField(default=-1)
    title = models.CharField(max_length=50)
    recipe_yield = models.CharField(max_length=50, default="")
    original_url = models.CharField(max_length=200, default="")

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient_info = models.CharField(max_length=100)

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    image_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

class Employee(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    office = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    start_date = models.DateField()
    salary = models.PositiveIntegerField()


    def __str__(self):
        return self.name
