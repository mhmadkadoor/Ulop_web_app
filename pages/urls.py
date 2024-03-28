from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.courses, name='courses'),
    path('sign/', views.sign, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/view/<int:post_id>/', views.view_post, name='view_post'),
    path('post/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment_page'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]