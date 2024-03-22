from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('groups/', views.groups, name='groups' ), # `name='home'` kwarg gives the route a name - naming is optional, but good practice (it will come in handy later)
]
