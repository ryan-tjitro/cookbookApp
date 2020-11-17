from django.urls import path
from list_recipes import views

urlpatterns = [
    path('', views.home, name='home'),
]
