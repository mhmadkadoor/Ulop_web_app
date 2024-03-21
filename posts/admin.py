from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender_name', 'catagory', 'date_posted', 'active')
    list_display_links = ('title',)
    list_editable = ('catagory',)
    list_filter = ('active', 'catagory')
    search_fields = ('title', 'content')

    
    

admin.site.register(Post, PostAdmin)
