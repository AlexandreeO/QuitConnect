from django.shortcuts import render, redirect

from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Group, UserPost, Meeting

def home(request):
    return render(request, 'home.html')

def group_detail(request, group_id):
    group = Group.objects.get(id=group_id)
    user = request.user
    print(user in group.members.all())
    return render(request, 'groups/group_detail.html', {
        'group': group,
        'user': user
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