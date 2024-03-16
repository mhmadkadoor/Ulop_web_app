from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'title', 'active', 'catagory','date_posted')
    list_display_links = ('title',)
    list_editable = ('active','catagory')
    list_filter = ("catagory", "active", "date_posted")
    search_fields = ['title', 'content', 'sender_name']
    fields=['title', 'content', 'image', 'active', 'catagory']



admin.site.register(Post, PostAdmin)
admin.site.site_header = 'ULOP Chat Admin'
admin.site.site_title = 'ULOP Chat'
