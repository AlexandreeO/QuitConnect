from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups' ), 
    path('accounts/signup/', views.signup, name='signup'),
    path('groups/<int:group_id>/join/', views.join_group, name='join_group'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/createpost/', views.PostCreate.as_view(), name='post_create'),
    path('groups/<int:pk>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('groups/<int:pk>/update/', views.PostUpdate.as_view(), name='post_update'),   
    path('groups/<int:group_id>/createmeeting/', views.CreateMeeting.as_view(), name='meeting_create'),
    path('groups/<int:group_id>/joinmeeting/', views.JoinMeeting, name='join_meeting'),
]

