from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
import uuid # needed for generating random IDs
import boto3 # AWS Python SDK
import os # needed for accessing env vars
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, UserPost, Photo, Meeting
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.forms import ModelForm, CharField, FileField

def home(request):
    return render(request, 'home.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    print(group.userpost_set.filter(user=user))
    
    
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'user': user,
    })


def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups/groups.html', {
        'groups': groups
        
    })


    
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

class PostCreateForm(ModelForm):
    class Meta:
        fields=['content']
        model = UserPost
        
    post_photo = FileField()


class PostCreate(CreateView):
    model = UserPost
    # fields=['content']
    form_class = PostCreateForm
    
    def form_valid(self, form):
        print(form)
        print(form.instance)
        # print(form.instance.photo_set)
        # print(form.instance.photo_file)
        print(self.form_class.post_photo)

        form.instance.user = self.request.user
        form.instance.group_id = self.kwargs['group_id'] 

        return super().form_valid(form)
class PostDelete(DeleteView):
    model = UserPost

    def get_success_url(self):
        group_id = self.object.group.id
        return reverse_lazy('group_detail', kwargs={'group_id': group_id})

class PostUpdate(UpdateView):
    model = UserPost
    fields = ['content'] 

    def get_success_url(self):
        group_id = self.object.group.id
        return reverse_lazy('group_detail', kwargs={'group_id': group_id})

def add_photo(request, group_name, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, post_id=post_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('group_detail', post_id=post_id)