from django.shortcuts import render

# Create your views here.

def home (request):
    return render(request, 'pages/htmls/home.html')
def about (request):
    return render(request, 'pages/htmls/about.html')
def courses (request):
    return render(request, 'pages/htmls/courses.html')