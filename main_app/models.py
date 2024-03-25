from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Group(models.Model):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=250)
    members=models.ManyToManyField(User, 'group_member')
    def __str__(self):
        return f'{self.name} ({self.description})'

class UserPost(models.Model):
    content=models.CharField(max_length=300)
    created_at = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.content}'

class Meeting(models.Model):
    date=models.DateField()
    time=models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')

    attendees = models.ManyToManyField(User, related_name='meeting_attendees')

    
    

