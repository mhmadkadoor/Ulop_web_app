from django.db import models
from datetime import datetime
# Create your models here.

class Post(models.Model):
    x= [
        ('News', 'News'),
        ('Question', 'Question'),
        ('Tips', 'Tips'),
        ('Event', 'Event'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posted_images/%Y/%m/%d/', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='posted date')
    sender_id = models.IntegerField(default=0, verbose_name='sender id')
    sender_name = models.CharField(max_length=100, default='', verbose_name='sender name')
    active = models.BooleanField(default=True, verbose_name='public post')
    catagory = models.CharField(max_length=100, null=True, blank=True, choices=x, verbose_name='catagory')
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "All Post"
        ordering = ['-date_posted']
