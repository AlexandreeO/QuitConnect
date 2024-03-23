from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups' ), # `name='home'` kwarg gives the route a name - naming is optional, but good practice (it will come in handy later)
    path('accounts/signup/', views.signup, name='signup'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
]

