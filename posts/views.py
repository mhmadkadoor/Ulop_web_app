from django.shortcuts import render
from .models import Post
# Create your views here.

def posts(request):
    return render(request, 'posts/posts.html', {'posts': Post.objects.all()})
def post(request):
    return render(request, 'posts/post.html')