from django.contrib import admin
from .models import Post, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'sender_name', 'catagory', 'date_posted', 'active')
    list_display_links = ('title',)
    list_editable = ('catagory',)
    list_filter = ('active', 'catagory')
    search_fields = ('title', 'content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id','sender_name', 'date_posted')
    list_display_links = ('sender_name',)
    search_fields = ('sender_name', 'content')



admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)
