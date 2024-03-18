from django.shortcuts import render
from posts.models import Post
# Create your views here.

def home (request):
    return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all()})
def about (request):
    return render(request, 'pages/htmls/about.html')
def courses (request):
    return render(request, 'pages/htmls/courses.html')