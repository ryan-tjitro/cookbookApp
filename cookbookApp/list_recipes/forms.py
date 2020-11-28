from django import forms
from django.contrib.auth.forms import UserCreationForm

class UrlForm(forms.Form):
    url = forms.URLField(label='url')

class CreateRecipeForm(forms.Form):
    title = forms.CharField(label="title")
    recipe_yield = forms.CharField(label="recipe_yield", required=False)
    time = forms.IntegerField(label="time", required=False)
    instructions = forms.CharField(label="instructions", widget=forms.Textarea, required=False)

class ImageForm(forms.Form):
    title = forms.CharField(max_length=100)
    image = forms.ImageField()

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="first_name")
    last_name = forms.CharField(label="last_name")
    email = forms.CharField(widget=forms.EmailInput)
    
class IngredientForm(forms.Form):
    ingredient = forms.CharField(label="ingredient", required=False)
