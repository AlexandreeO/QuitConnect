from django.shortcuts import render, redirect
from django.urls import reverse_lazy
import uuid # needed for generating random IDs
import boto3 # AWS Python SDK
import os # needed for accessing env vars

from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, UserPost, Meeting, Photo
from django.views.generic.edit import CreateView, DeleteView, UpdateView

def home(request):
    return render(request, 'home.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    
    
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'user': user,
        
    })


def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups.html', {
        'groups': groups
        
    })


@login_required
def join_group(request, group_id):
        group = Group.objects.get(id=group_id)
        user = request.user
        group.members.add(user)
        group.save()
        print(group.members.all())
        return redirect('group_detail', group_id=group_id)
    

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
    
            user = form.save()
    
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class PostCreate(CreateView):
    model = UserPost
    fields=['content']

    def form_valid(self, form): 
        print(self)
        print(self.model)
        print(self.model.group)
        form.instance.user = self.request.user
        form.instance.group_id = self.kwargs['group_id']
        self.object = form.save()
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex + photo_file.name
            bucket = os.environ['S3_BUCKET']

            try:
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                Photo.objects.create(url=url, post=self.object)
            except Exception as e:
                print('An error occurred uploading file to S3:', e)
                # Consider handling the error appropriately

        return super().form_valid(form)
class PostDelete(DeleteView):
    model = UserPost

    def get_success_url(self):
        group_id = self.object.group.id
        return reverse_lazy('group_detail', kwargs={'group_id': group_id})

class PostUpdate(UpdateView):
    model = UserPost
    fields = ['content'] 
    def form_valid(self, form):
        self.object = form.save()
        
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex + photo_file.name
            bucket = os.environ['S3_BUCKET']

            try:
                s3.upload_fileobj(photo_file, bucket, key)
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                
                # Here you can decide to update the existing photo or create a new one
                photo, created = Photo.objects.update_or_create(
                    post=self.object,
                    defaults={'url': url}
                )
            except Exception as e:
                print('An error occurred uploading file to S3:', e)
                # Handle the error appropriately

        return super().form_valid(form)

    def get_success_url(self):
        group_id = self.object.group.id
        return reverse_lazy('group_detail', kwargs={'group_id': group_id})

class CreateMeeting(CreateView):
    model = Meeting
    fields = ['name', 'date', 'start_time', 'end_time']
    
    def get_success_url(self):
        group_id = self.object.group.id
        return reverse_lazy('group_detail', kwargs={'group_id': group_id})
        
    
    def form_valid(self, form):
        form.instance.host = self.request.user
        form.instance.group_id = self.kwargs['group_id']
        print(form.instance)

        return super().form_valid(form)




def JoinMeeting(request, meeting_id):
    pass