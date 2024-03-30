from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


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
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f'{self.content}'
    
    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'group_id': self.group.id})

class Meeting(models.Model):
    date=models.DateField()
    time=models.TimeField()
    created_at = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_meetings')

    attendees = models.ManyToManyField(User, related_name='meeting_attendees')

    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE) # ForeignKey for the Cat the Photo belongs to

    def __str__(self):
<<<<<<< HEAD
        return f"Photo for post_id: {self.post.id} @{self.url}"
=======
        return f"Photo for post_id: {self.post_id} @{self.url}"
>>>>>>> refs/remotes/origin/main

