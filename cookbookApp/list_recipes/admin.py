from django.contrib import admin
from .models import Employee, Recipe, Ingredient


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Employee._meta.fields]

class RecipeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Recipe._meta.fields]

# class UserAdmin(admin.ModelAdmin):
#     list_display = [f.name for f in User._meta.fields]

class IngredientAdmin(admin.ModelAdmin):
     list_display = [f.name for f in Ingredient._meta.fields]


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(User, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
# Register your models here.
