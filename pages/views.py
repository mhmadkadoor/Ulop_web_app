from django.shortcuts import render
from posts.models import Post
from .models import Login
from .forms import LoginForm

# Create your views here.

def home (request):
    return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all()})

def about (request):
    return render(request, 'pages/htmls/about.html')

def courses (request):
    return render(request, 'pages/htmls/courses.html')

def login (request):
    dataform = LoginForm(request.POST)
    if request.method == 'POST':
        if dataform.is_valid():
            dataform.save()
    
    return render(request, 'pages/htmls/login.html', {'Lf': LoginForm()})

def sign (request):
    return render(request, 'pages/htmls/sign.html')
