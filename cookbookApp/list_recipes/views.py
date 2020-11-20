from django.shortcuts import render
from list_recipes.forms import UrlForm, CreateRecipeForm, UserRegistrationForm
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Employee, Recipe, Ingredient
from recipe_scrapers import scrape_me, WebsiteNotImplementedError
import logging

# Create your views here.
class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        recipes = Recipe.objects.filter(user = request.user)
        return render(request, self.template, {'recipes': recipes})

class AddAutomatic(LoginRequiredMixin, View):
    template = 'addAutomatic.html'
    login_url = '/login/'
    WEBSITE_NOT_IMPLEMENTED = "Cooking Journal cannot currently extract recipes from this website!"
    RECIPE_EXISTS = "Recipe with the same title exists!"

    def get(self, request):
        form = UrlForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        url = request.POST.get('url', None)
        if url is not None:
           try:
               scraper = scrape_me(url)
               existing_recipe = Recipe.objects.filter(user = request.user).get(original_url = url)
               return render(request, self.template, {'form': UrlForm(request.POST), "success": False, "errorReason": self.RECIPE_EXISTS}) #with error
           except Recipe.DoesNotExist:
               new_recipe = Recipe.objects.create(user = request.user, instructions = scraper.instructions(), time = scraper.total_time(), title = scraper.title(), recipe_yield = scraper.yields(), original_url = url)
               for ingredient_description in scraper.ingredients():
                   new_ingredient = Ingredient.objects.create(recipe=new_recipe, ingredient_info=ingredient_description)
                   logging.debug("ingredient: {0}".format(ingredient_description))
               return render(request, self.template, {'form': UrlForm(), "success": True})
           except WebsiteNotImplementedError:
               return render(request, self.template, {'form': UrlForm(request.POST), "success": False, "errorReason": self.WEBSITE_NOT_IMPLEMENTED})

class AddManually(LoginRequiredMixin, View):
    template = 'addManually.html'
    login_url = '/login/'
    RECIPE_EXISTS = "Recipe with the same title exists!"
    INVALID_TITLE = "Please choose a different name!"

    def get(self, request):
        form = CreateRecipeForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        title = request.POST.get('title', "")
        recipe_yield = request.POST.get("recipe_yield", None)
        time = request.POST.get("time", "")
        if len(time) == 0:
            time = -1
        else:
            time = int(time)
        instructions = request.POST.get("instructions", None)
        if len(title) > 0:
           try:
               existing_recipe = Recipe.objects.filter(user = request.user).get(title = title)
               return render(request, self.template, {'form': CreateRecipeForm(request.POST), "success": False, "errorReason": self.RECIPE_EXISTS}) #with error bc title already exists
           except Recipe.DoesNotExist:
               new_recipe = Recipe.objects.create(user = request.user, time=time, instructions = instructions, title = title, recipe_yield = recipe_yield)
               # for ingredient_description in scraper.ingredients():
               #     new_ingredient = Ingredient.objects.create(recipe=new_recipe, ingredient_info=ingredient_description)
               #     logging.debug("ingredient: {0}".format(ingredient_description))
               return render(request, self.template, {'form': U(), "success": True})
        else:
            return render(request, self.template, {'form': CreateRecipeForm(), "success": False, "errorReason": self.INVALID_TITLE}) #with error bc invalid name

class Login(View):
    template = 'login.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template, {'form': form})


    def post(self, request):
        form = AuthenticationForm(request.POST)
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template, {'form': form})

class Test(View):
    template = 'testing.html'

    def get(self, request, title):
        recipe = Recipe.objects.filter(user = request.user).get(title = title)
        ingredients = Ingredient.objects.filter(recipe = recipe)
        logging.debug(ingredients)
        return render(request, self.template, {'recipe': recipe, 'ingredients': ingredients})

class UserRegistration(View):
    template = "UserRegistration.html"
    PASSWORD_MISMATCH = "Passwords don't match!"
    INVALID_FIELDS = "Invalid fields. Please try again!"
    USERNAME_IN_USE = "A user with this name already exists!"
    EMAIL_IN_USE = "This email has already been associated with another account!"

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if not form.is_valid():
            try:
                password = form.clean_password2()
            except ValidationError:
                return render(request, self.template, {'form': form,  "errorReason": self.PASSWORD_MISMATCH})
            if len(User.objects.filter(username = request.POST.get("username", ""))):
                return render(request, self.template, {'form': form,  "errorReason": self.USERNAME_IN_USE})
            if len(User.objects.filter(email = request.POST.get("email", ""))):
                return render(request, self.template, {'form': form,  "errorReason": self.EMAIL_IN_USE})
            return render(request, self.template, {'form': form,  "errorReason": self.INVALID_FIELDS})
        else:
            password = request.POST.get("password1", False)
            username = request.POST.get("username", False)
            first_name = request.POST.get("first_name", False)
            last_name = request.POST.get("last_name", False)
            email = request.POST.get("email", False)
            logging.debug("values are not problem")
            user= User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            return HttpResponseRedirect('/')
