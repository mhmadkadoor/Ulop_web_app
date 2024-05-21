from django.shortcuts import render
from posts.models import Post, Comment
from django.db import transaction
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponseNotFound
import os
# Create your views here.

def view_post(request, post_id):
    comments = Comment.objects.all()
    current_post = Post.objects.get(id=post_id)
    current_user = request.user

    return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments, "thisPage": 'view_post'})

@transaction.atomic
def edit_post(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_user = request.user

    
    if request.method == 'POST':
        if 'btnPostEdite' in request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            category = request.POST.get('category')
            visibility = request.POST.get('visibility')
            active = visibility == 'public'
            image = request.FILES.get('image')
            pdf = request.FILES.get('pdf')

            # Delete the old image if a new image is uploaded
            if image and current_post.image:
                old_image_path = current_post.image.path
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)

            # Delete the old PDF if a new PDF is uploaded
            if pdf and current_post.pdf:
                old_pdf_path = current_post.pdf.path
                if os.path.isfile(old_pdf_path):
                    os.remove(old_pdf_path)

            current_post.title = title
            current_post.content = content
            current_post.category = category
            current_post.active = active
            if image:
                current_post.image = image
            if pdf:
                current_post.pdf = pdf
            current_post.save()
            return redirect('profile')  # Assuming you have a 'profile' named URL pattern

        elif 'btnPostDelete' in request.POST:
            current_post.delete()
            return redirect('profile')  # Assuming you have a 'profile' named URL pattern

    else:
        return render(request, 'posts/edit_post.html', {'post': current_post, "thisPage": 'edit_post'})




def home(request):
    current_user = request.user

    comments = Comment.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        pdf = request.FILES.get('pdf')  # Get the PDF from the request
        sender_id = current_user.id

        if not current_user.first_name and not current_user.last_name:
            sender_name = current_user.username
        else:
            sender_name = f"{current_user.first_name} {current_user.last_name}"
        active = request.POST.get('visibility') == 'public'

        # Check if a post with the same title, content, and sender_id already exists
        if not Post.objects.filter(title=title, content=content, sender_id=sender_id).exists():
            post = Post(title=title, content=content, category=category, sender_id=sender_id, sender_name=sender_name, active=active, owner=current_user)
            if image:
                post.image = image
            if pdf:
                post.pdf = pdf
            post.save()

        return render(request, 'pages/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments , 'thisPage': 'home'})
    else:
        return render(request, 'pages/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments, 'thisPage': 'home'})

def about (request):
    current_user = request.user

    return render(request, 'pages/about.html',{ 'thisPage': 'about'})

@transaction.atomic
@login_required(login_url='login')
def profile (request):
    profileReturn = Profile.objects.get_or_create(user=request.user)[0]
    current_user = request.user

    if request.method == 'POST':
        if 'btnMailChange' in request.POST:
            if str(request.POST.get('NewMail')) == 'None':
                return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'None_input': True, 'thisPage': 'profile'})
            elif str(request.POST.get('NewMail')) == current_user.email:
                return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'email_exists': True, 'thisPage': 'profile'})
            else:
                current_user.email = request.POST.get('NewMail')
                current_user.save()
                return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'email_changed': True, 'thisPage': 'profile'})
        elif 'btnPassChange' in request.POST:
            password = request.POST.get('current_password')
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')
            if current_user.check_password(password):
                if password1 == password2:
                    current_user.set_password(password1)
                    current_user.save()
                    user = authenticate(request, username=current_user.username, password=password1)
                    auth.login(request, user)
                    return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user, 'password_changed': True, 'thisPage': 'profile'})
                else:
                    return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user, 'passwords_not_match': True, 'thisPage': 'profile'})
            else:
                return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user, 'password_incorrect': True, 'thisPage': 'profile'})
        elif 'btnDeleteAccount' in request.POST:
            current_user.delete()
            return redirect('home')
        elif 'btnUpdateProfile' in request.POST:
            # Handle profile update logic
            if 'image' in request.FILES:
                # Get the current profile
                profile = Profile.objects.get(user=current_user)
                # Check if the user already has a profile picture
                if profile.image and profile.image != 'profile_pics/male_def.jpg':
                    # Delete the old profile picture
                    profile.image.delete()
                # Save the new profile picture
                profile.image = request.FILES['image']
                profile.save()
                messages.success(request, 'Profile picture updated successfully.')
            else:
                messages.error(request, 'No image selected for upload.')
            return redirect('profile')
        
    return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'thisPage': 'profile'})



def view_profile(request, user_id):
    current_user = request.user

    return render(request, 'pages/view_profile.html', {'user': current_user, 'posts': Post.objects.all(), 'profilo': User.objects.get(id=user_id),})

@transaction.atomic
def sign(request):
    if request.method == 'POST':
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        confirm_password = str(request.POST.get('confirm_password'))
        first_name = str(request.POST.get('first_name'))
        last_name = str(request.POST.get('last_name'))
        email = str(request.POST.get('email'))
        if str(password) != str(confirm_password):
            return render(request, 'pages/sign.html', {'passwords_not_match': True, 'user_already_exists': False,'account_created': False, "thisPage": 'sign'})
        else:
            users_list = User.objects.all()
            for i in range(len(users_list)):
                if str(users_list[i]) == str(username):
                    user_already_exist = True
                    break
                else:
                    user_already_exist = False
                # Add code to check if the user exists in the database
    
            if user_already_exist:
            # Return user_already_exist as true
                return render(request, 'pages/sign.html', {'passwords_not_match': False,'user_already_exists': True,'account_created': False, "thisPage": 'sign'})
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                userProfile = Profile(user=user)
                user.save()
                userProfile.save()
                return render(request, 'pages/sign.html', {'passwords_not_match': False,'user_already_exists': False ,'account_created': True, "thisPage": 'sign'})
    else:  
        return render(request, 'pages/sign.html', {'passwords_not_match': False,'user_already_exists': False,'account_created': False, "thisPage": 'sign' })

def login(request):
    current_user = request.user

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        users_list = User.objects.all()
        for i in range(len(users_list)):
            if str(users_list[i]) == str(username):
                user_exists = True
                break
            else:
                user_exists = False

        if user_exists:
            user_1 = User.objects.get(username=username)
            if user_1.check_password(password):
                user = authenticate(request, username=username, password=password)
                auth.login(request, user)
                return render(request, 'pages/login.html', {'logged_in': True, 'user': current_user, "thisPage": 'login'})
            else:
                return render(request, 'pages/login.html', {'password_not_match': True, "thisPage": 'login'})
        else:
            return render(request, 'pages/login.html', {'user_not_exists': True, "thisPage": 'login'})
    else:
        return render(request, 'pages/login.html',{ "thisPage": 'login'})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')

def add_comment(request, post_id):
    current_post = Post.objects.get(id=post_id)
    comments = current_post.comments.all()
    current_user = request.user

    if request.method == 'POST':
        content = request.POST.get('comment_content').strip()
        sender_id = current_user.id

        if not content:
            return redirect('view_post', post_id=post_id)  

        if current_user.first_name == '' and current_user.last_name == '':
            sender_name = current_user.username
        else:
            sender_name = f"{current_user.first_name} {current_user.last_name}"

        is_unique_comment = not Comment.objects.filter(content=content, sender_id=sender_id, post=current_post, owner=current_user).exists()

        if is_unique_comment:
            Comment.objects.create(post=current_post, content=content, sender_id=sender_id, sender_name=sender_name, owner=current_user)

        return redirect('view_post', post_id=post_id)  
    else:
        return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments})
    
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    comment.delete()
    return render(request, 'posts/view_post.html', {'post': post, 'comments': Comment.objects.all(), 'thisPage': 'view_post'})

def edit_comment(request, comment_id):
    current_user = request.user

    comments = Comment.objects.all()
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    if request.method == 'POST':
        content = str(request.POST.get('comment_content'))
        comment.content = content
        comment.owner = current_user
        is_unique_comment = True
        for existing_comment in comments:
            if (existing_comment.content == content) and (existing_comment.sender_id == comment.sender_id) and (existing_comment.post == post):
                is_unique_comment = False
                break
        if is_unique_comment:
            comment.save()
        return render(request, 'posts/view_post.html', {'post': post, 'comments': Comment.objects.all(), 'thisPage': 'view_post'})
    else:
        return render(request, 'posts/edit_comment.html', {'comment': comment, 'user': current_user , 'thisPage': 'edit_comment'})
    
def custom_page_not_found_view(request, exception):
    return render(request, '404.html')

def custom_error_view(request):
    return render(request, '500.html')