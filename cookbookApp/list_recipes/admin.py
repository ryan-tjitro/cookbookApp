from django.contrib import admin
from .models import Employee, Recipe, RecipeImage, Ingredient


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]

class RecipeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Recipe._meta.fields]

class RecipeImageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in RecipeImage._meta.fields]

class IngredientAdmin(admin.ModelAdmin):
     list_display = [f.name for f in Ingredient._meta.fields]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeImage, RecipeImageAdmin)
admin.site.register(Ingredient, IngredientAdmin)
# Register your models here.
