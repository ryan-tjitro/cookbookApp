from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=50)
#     email = models.CharField(max_length=100)
#     password = models.CharField(max_length=50)

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#
#     def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             UserProfile.objects.create(user=instance)
#         post_save.connect(create_user_profile, sender=User)

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

class Employee(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    office = models.CharField(max_length=150)
    age = models.PositiveIntegerField()
    start_date = models.DateField()
    salary = models.PositiveIntegerField()


    def __str__(self):
        return self.name
