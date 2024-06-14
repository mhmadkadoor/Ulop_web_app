from django.shortcuts import render
from posts.models import Post, Comment
from django.db import transaction
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.conf import settings
import os
# Create your views here.

BAD_WORDS = [
    "sex", "fuck", "fucking", "shit", "puta", "bitch", "ass", "motherfucker", 
    "cunt", "whore", "bastard", "crap", "damn", "faggot", "asswipe", 
    "douchebag", "piss", "cock", "niga", "nigger", "pussy", "naked",
    "dick", "asshole", "slut", "bollocks", "arse", "bugger",
    "bloody", "c**t", "screw", "wanker", "knobhead", "tosser", "bellend",
    "twat", "prick", "dipshit", "dumbass", "bullshit", "freaking",
    "shitfaced", "assclown", "cockwomble",
    "fuckwit", "dickhead", "piss off", "dickwad", "twatwaffle",
    "fuckface", "fuckery", "clusterfuck", "assface", "shitstorm",
    "butt munch", "cuntnugget", "ass goblin", "piss flaps", "cock jockey",
    "dick cheese", "twat nugget", "wank stain", "cunt nugget", "arse biscuit",
    "shit biscuit", "wank nugget", "fuck nugget", "crap basket", "fuck bucket",
    "douche nozzle", "shit waffle", "ass monkey", "shit monkey", "cock gobbler",
    "fart knocker", "dick muncher", "cum dumpster", "asshatery", "fucknuttery",
    "cuntbiscuit", "cock juggling thundercunt", "piss wizard", "fuck trumpet",
    "shit rocket", "fucknugget", "twatwaffle", "douchecanoe",
    "shit goblin", "asshatery", "fucknuttery", "shitlord", "cockwomble",
    "assmunch", "dickbag", "fuckboy", "fucknut", "shitforbrains", "asswipe",
    "shitbag", "douche rocket", "wanker", "fucktard", "douchelord", "fart face",
    "cockgoblin", "fuckstick", "dickwaffle", "twatwad", "shitbird", "dickweed",
    "cuntface"
]

def filter_bad_words(content):
    """
    Filters out bad words from the content.
    """
    words = content.split()
    filtered_words = []

    for word in words:
        if word.lower() in BAD_WORDS:
            # Replace bad words with asterisks
            filtered_words.append("*" * len(word))
        else:
            filtered_words.append(word)

    return " ".join(filtered_words)

def view_post(request, post_id):
    comments = Comment.objects.all()
    current_post = Post.objects.get(id=post_id)

    return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments, "thisPage": 'view_post'})

@transaction.atomic
def edit_post(request, post_id):
    current_post = Post.objects.get(id=post_id)
    current_user = request.user

    
    if request.method == 'POST':
        if 'btnPostEdit' in request.POST:
            title = request.POST.get('title')
            filtered_title = filter_bad_words(title)
            content = request.POST.get('content')
            filtered_content = filter_bad_words(content)
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

            current_post.title = filtered_title
            current_post.content = filtered_content
            current_post.category = category
            current_post.active = active
            if image:
                current_post.image = image
            if pdf:
                current_post.pdf = pdf
            current_post.save()
            return redirect('view_post', post_id=post_id)  

        elif 'btnPostDelete' in request.POST:
            current_post.delete()
            return redirect('profile') 
        elif 'btnPdfDelete' in request.POST:
            if current_post.pdf:
                folder_path = os.path.join(settings.MEDIA_ROOT, f"posted_pdfs/{current_post.date_posted.strftime('%Y/%m/%d')}")
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(folder_path)
                current_post.pdf.delete()
            current_post.save()
            return render(request, 'posts/edit_post.html', {'post': current_post, "thisPage": 'edit_post'})
        elif 'btnImageDelete' in request.POST:
            if current_post.image:
                folder_path = os.path.join(settings.MEDIA_ROOT, f"posted_images/{current_post.date_posted.strftime('%Y/%m/%d')}")
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, filename)
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                    os.rmdir(folder_path)
                current_post.image.delete()
            current_post.save()
            return render(request, 'posts/edit_post.html', {'post': current_post, "thisPage": 'edit_post'})
        elif 'btnCancel' in request.POST:
            return redirect('view_post', post_id=post_id) 

    else:
        return render(request, 'posts/edit_post.html', {'post': current_post, "thisPage": 'edit_post'})
    


def home(request):
    current_user = request.user

    comments = Comment.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title').strip()
        filtered_title = filter_bad_words(title)
        content = request.POST.get('content').strip()
        filtered_content = filter_bad_words(content)
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
        if not Post.objects.filter(title=filtered_title, content=filtered_content, sender_id=sender_id).exists():
            post = Post(title=filtered_title, content=filtered_content, category=category, sender_id=sender_id, sender_name=sender_name, active=active, owner=current_user)
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
            current_user_posts = Post.objects.filter(owner=current_user)
            for post in current_user_posts:
                post.delete()
            current_user_profile = Profile.objects.get(user=current_user)
            current_user_posts.delete()
            if current_user_profile.image != 'profile_pics/male_def.jpg':
                current_user_profile.delete()
            current_user.delete()
            return redirect('home')
        elif 'btnUpdateProfile' in request.POST:
            
            if 'image' in request.FILES:

                profile = Profile.objects.get(user=current_user)

                if profile.image and profile.image != 'profile_pics/male_def.jpg':

                    profile.image.delete()

                profile.image = request.FILES['image']
                profile.save()
                messages.success(request, 'Profile picture updated successfully.')
            else:
                messages.error(request, 'No image selected for upload.')
            return redirect('profile')
        elif 'btnUpdateBio' in request.POST:
            bio = request.POST.get('bio')
            profile = Profile.objects.get(user=current_user)
            if len(bio) > 400:
                return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'thisPage': 'profile', 'bio_long': True})
            profile.bio = bio
            profile.save()
            messages.success(request, 'Bio updated successfully.')
            return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'thisPage': 'profile', 'bio_updated': True})
        
    return render(request, 'pages/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'thisPage': 'profile'})



def view_profile(request, user_id):
    current_user = request.user

    return render(request, 'pages/view_profile.html', {'user': current_user, 'posts': Post.objects.all(), 'profilo': User.objects.get(id=user_id), 'thisPage': 'view_profile'})

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
    
            if user_already_exist:
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

@login_required(login_url='home')
def logout(request):
    auth.logout(request)
    return redirect('home')

def add_comment(request, post_id):
    current_post = Post.objects.get(id=post_id)
    comments = current_post.comments.all()
    current_user = request.user

    if request.method == 'POST':
        content = request.POST.get('comment_content').strip()
        filtered_content = filter_bad_words(content)
        sender_id = current_user.id

        if not content:
            return redirect('view_post', post_id=post_id)  

        if current_user.first_name == '' and current_user.last_name == '':
            sender_name = current_user.username
        else:
            sender_name = f"{current_user.first_name} {current_user.last_name}"

        is_unique_comment = not Comment.objects.filter(content=filtered_content, sender_id=sender_id, post=current_post, owner=current_user).exists()

        if is_unique_comment:
            Comment.objects.create(post=current_post, content=filtered_content, sender_id=sender_id, sender_name=sender_name, owner=current_user)

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
        content = str(request.POST.get('comment_content')).strip()
        filtered_content = filter_bad_words(content)
        comment.content = content
        is_unique_comment = True
        for existing_comment in comments:
            if (existing_comment.content == filtered_content) and (existing_comment.sender_id == comment.sender_id) and (existing_comment.post == post):
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

