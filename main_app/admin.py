from django.contrib import admin
from .models import Group, UserPost, Photo, Meeting

# Register your models here.
admin.site.register(Group)
admin.site.register(UserPost)
admin.site.register(Photo)
admin.site.register(Meeting)