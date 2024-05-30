from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
# Create your models here.

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('News', 'News'),
        ('Question', 'Question'),
        ('Tips', 'Tips'),
        ('Event', 'Event'),
        ('Other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='owner')
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='posted_images/%Y/%m/%d/', null=True, blank=True)
    pdf = models.FileField(upload_to='posted_pdfs/%Y/%m/%d/', null=True, blank=True, verbose_name='PDF file')
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='posted date')
    sender_id = models.IntegerField(default=0, verbose_name='sender id')
    sender_name = models.CharField(max_length=100, default='', verbose_name='sender name')
    active = models.BooleanField(default=True, verbose_name='public post')
    category = models.CharField(max_length=100, null=True, blank=True, choices=CATEGORY_CHOICES, verbose_name='category')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file and its folder
        if self.image:
            folder_path = os.path.join(settings.MEDIA_ROOT, f"posted_images/{self.date_posted.strftime('%Y/%m/%d')}")
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(folder_path)

        # Delete the PDF file and its folder
        if self.pdf:
            folder_path = os.path.join(settings.MEDIA_ROOT, f"posted_pdfs/{self.date_posted.strftime('%Y/%m/%d')}")
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(folder_path)

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "All Post"
        ordering = ['-date_posted']



class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name='owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    sender_id = models.IntegerField(default=1, verbose_name='sender id')
    sender_name = models.CharField(max_length=100, default='', verbose_name='sender name')
    content = models.TextField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name='posted date')
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = "All Comment"
        ordering = ['-date_posted']