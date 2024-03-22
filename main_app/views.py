from django.shortcuts import render


def index(request):
    return render(request, 'index.html')

def groups(request):
    return render(request, 'groups.html')