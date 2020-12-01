from django.shortcuts import render
from list_recipes.forms import UrlForm, CreateRecipeForm, UserRegistrationForm
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.formsets import formset_factory
from .models import Employee, Recipe, Ingredient, RecipeImage
from .forms import CreateRecipeForm, ImageForm, IngredientForm, UrlForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from recipe_scrapers import scrape_me, WebsiteNotImplementedError
import logging

def addImage(request, title):
    def addImage():
        form = ImageForm(request.POST, request.FILES)
        recipe = Recipe.objects.filter(user = request.user).get(title = title)
        ingredients = Ingredient.objects.filter(recipe = recipe)
        if form.is_valid():
            image_title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            RecipeImage.objects.create(recipe=recipe, image_title = image_title, image=image)
        logging.debug('invalid form:')
        logging.debug(form.errors)

    if request.method == 'POST':
        addImage()
    return HttpResponseRedirect('/test/' + title)

# Create your views here.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

class Index(LoginRequiredMixin, View):
    template = 'index.html'
    login_url = '/login/'

    def get(self, request):
        IngredientFormSet = formset_factory(IngredientForm)
        recipes = Recipe.objects.filter(user = request.user)
        return render(request, self.template, {'recipes': recipes, 'formset': IngredientFormSet()})

    def post(self, request):
        IngredientFormSet = formset_factory(IngredientForm)
        ingredients = IngredientFormSet(request.POST)
        if ingredients.is_valid():
            recipes = Recipe.objects.filter(user = request.user)
            for ingredient_form in ingredients:
                if ingredient_form.is_valid() and ingredient_form.cleaned_data.get('ingredient'):
                    recipes = recipes.filter(ingredient__ingredient_info__icontains=ingredient_form.cleaned_data.get('ingredient'))
                    logging.debug(recipes)
            return render(request, self.template, {'recipes': recipes.distinct(), 'formset': ingredients})
        return self.get(request)

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
        IngredientFormSet = formset_factory(IngredientForm)
        return render(request, self.template, {'formset': IngredientFormSet(), 'form': form})

    def post(self, request):
        IngredientFormSet = formset_factory(IngredientForm)
        ingredients = IngredientFormSet(request.POST)
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
               return render(request, self.template, {'formset': IngredientFormSet(request.POST), 'form': CreateRecipeForm(request.POST), "success": False, "errorReason": self.RECIPE_EXISTS}) #with error bc title already exists
           except Recipe.DoesNotExist:
               new_recipe = Recipe.objects.create(user = request.user, time=time, instructions = instructions, title = title, recipe_yield = recipe_yield)
               for ingredient_form in ingredients:
                   if ingredient_form.is_valid() and ingredient_form.cleaned_data.get('ingredient'):
                       new_ingredient = Ingredient.objects.create(recipe=new_recipe, ingredient_info=ingredient_form.cleaned_data.get('ingredient'))
               return render(request, self.template, {'formset': IngredientFormSet(), 'form': CreateRecipeForm(), "success": True})
        else:
            return render(request, self.template, {'formset': IngredientFormSet(request.POST), 'form': CreateRecipeForm(request.POST), "success": False, "errorReason": self.INVALID_TITLE}) #with error bc invalid name

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
            return render(request, self.template, {'form': form, 'login_failed': True})

class Test(View):
    template = 'testing.html'

    def get(self, request, title):
        recipe = Recipe.objects.filter(user = request.user).get(title = title)
        ingredients = Ingredient.objects.filter(recipe = recipe)
        images = RecipeImage.objects.filter(recipe = recipe)
        edit_recipe_form = CreateRecipeForm(initial={'title': recipe.title, 'time': recipe.time, 'recipe_yield': recipe.recipe_yield, 'instructions': recipe.instructions})
        IngredientFormSet = formset_factory(IngredientForm)
        ingredientForms = IngredientFormSet(initial=[{'ingredient': ingredient.ingredient_info} for ingredient in ingredients])
        recipe.instructions = recipe.instructions.split('\n')
        return render(request, self.template, {'images': images, 'recipe': recipe, 'ingredients': ingredients, 'image_upload_form': ImageForm(), 'edit_recipe_form': edit_recipe_form, 'ingredient_formset': ingredientForms})

    def post(self, request, title):
        form = CreateRecipeForm(request.POST)
        IngredientFormSet = formset_factory(IngredientForm)
        ingredient_forms = IngredientFormSet(request.POST)
        def updateRecipe():
            time = int(request.POST['time']) if len(request.POST['time']) > 0 else -1
            existing_recipe = Recipe.objects.filter(user = request.user).get(title = title)
            existing_recipe.title = request.POST['title']
            existing_recipe.recipe_yield = request.POST['recipe_yield']
            existing_recipe.time = time
            existing_recipe.instructions = request.POST['instructions']
            existing_recipe.save()

        def updateIngredients():
            existing_recipe = Recipe.objects.filter(user = request.user).get(title = title)
            new_ingredients = [ingredient_form.cleaned_data.get('ingredient') for ingredient_form in ingredient_forms if ingredient_form.is_valid() and ingredient_form.cleaned_data.get('ingredient')]
            existing_ingredient_objects = Ingredient.objects.filter(recipe = existing_recipe)
            existing_ingredients = [ingredient.ingredient_info for ingredient in existing_ingredient_objects]
            to_add = [ingredient for ingredient in new_ingredients if ingredient not in existing_ingredients]
            to_delete = [ingredient for ingredient in existing_ingredients if ingredient not in new_ingredients]
            for ingredient in to_add:
                Ingredient.objects.create(recipe=existing_recipe, ingredient_info=ingredient)
            existing_ingredient_objects.filter(ingredient_info__in=to_delete).delete()

        if form.is_valid():
            updateRecipe()
            updateIngredients()
        return self.get(request, title)

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
