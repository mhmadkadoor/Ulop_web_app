from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posted_images/%Y/%m/%d/')
    date_posted = models.DateTimeField(auto_now_add=True)
    sender_id = models.IntegerField()
    sender_name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    