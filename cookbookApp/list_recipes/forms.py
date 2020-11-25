from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label='url')

class CreateRecipeForm(forms.Form):
    title = forms.CharField(label="title")
    recipe_yield = forms.CharField(label="recipe_yield", required=False)
    time = forms.IntegerField(label="time", required=False)
    instructions = forms.CharField(label="instructions", widget=forms.Textarea, required=False)
    # ingredients =

class ImageForm(forms.Form):
    title = forms.CharField(max_length=100)
    image = forms.ImageField()
