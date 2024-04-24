from django.shortcuts import render
from posts.models import Post, Comment
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def view_post(request, post_id):
    comments = Comment.objects.all()
    current_post = Post.objects.get(id=post_id)
    return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments})

def edit_post(request, post_id):
    current_post = Post.objects.get(id=post_id)
    
    if request.method == 'POST':
        if 'btnPostEdite' in request.POST:
            title = str(request.POST.get('title'))
            content = str(request.POST.get('content'))
            image = request.FILES.get('image')
            catagory = request.POST.get('catagory')
            if str(request.POST.get('visibility')) == 'public':
                active = True
            else:
                active = False

            current_post.title = title
            current_post.content = content
            current_post.catagory = catagory
            current_post.active = active
            if image:
                current_post.image = image
            current_post.save()
            return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': request.user , 'UserS': User.objects.all()})
        elif 'btnPostDelete' in request.POST:
            current_post.delete()
            return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': request.user , 'UserS': User.objects.all()})
    else:
        return render(request, 'posts/edit_post.html', {'post': current_post})



def home (request):
    current_user = request.user
    comments = Comment.objects.all()
    if request.method == 'POST':
        title = str(request.POST.get('title'))
        content = str(request.POST.get('content'))
        image = request.FILES.get('image')
        catagory = request.POST.get('catagory')
        sender_id = current_user.id
        if current_user.first_name == '' and current_user.last_name == '':
            sender_name = current_user.username
        else:
            sender_name = f"{current_user.first_name} {current_user.last_name}"
        print(f'image: {image}, image type: {type(image)}')
        if str(request.POST.get('visibility')) == 'public':
            active = True
        else:
            active = False

        post = Post(title=title, content=content, catagory=catagory, sender_id=sender_id, sender_name=sender_name, active=active, owner=current_user)
        if image:
            post.image = image
        postes = Post.objects.all()
        for i in range(len(postes)):
            if postes[i].title != title and postes[i].content != content:
                post.save()
                return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments})
            return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments})
        else:
            return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments})
    else:
        return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all(), 'user': current_user, 'comments': comments})

def about (request):
    return render(request, 'pages/htmls/about.html')
def courses (request):
    return render(request, 'pages/htmls/courses.html')

@login_required(login_url='login')
def profile (request):
    current_user = request.user
    if request.method == 'POST':
        if 'btnMailChange' in request.POST:
            if str(request.POST.get('NewMail')) == 'None':
                return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'None_input': True})
            elif str(request.POST.get('NewMail')) == current_user.email:
                return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'email_exists': True})
            else:
                current_user.email = request.POST.get('NewMail')
                current_user.save()
                return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all(), 'email_changed': True})
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
                    return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user, 'password_changed': True})
                else:
                    return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user, 'passwords_not_match': True})
            else:
                return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user, 'password_incorrect': True})
        elif 'btnDeleteAccount' in request.POST:
            current_user.delete()
            return redirect('home')
        
    return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all()})

def sign(request):
    if request.method == 'POST':
        username = str(request.POST.get('username'))
        password = str(request.POST.get('password'))
        confirm_password = str(request.POST.get('confirm_password'))
        first_name = str(request.POST.get('first_name'))
        last_name = str(request.POST.get('last_name'))
        email = str(request.POST.get('email'))
        if str(password) != str(confirm_password):
            return render(request, 'pages/htmls/sign.html', {'passwords_not_match': True, 'user_already_exists': False,'account_created': False})
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
                return render(request, 'pages/htmls/sign.html', {'passwords_not_match': False,'user_already_exists': True,'account_created': False})
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                user.save()
                return render(request, 'pages/htmls/sign.html', {'passwords_not_match': False,'user_already_exists': False ,'account_created': True})
    else:  
        return render(request, 'pages/htmls/sign.html', {'passwords_not_match': False,'user_already_exists': False,'account_created': False })

def login(request):
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
                return render(request, 'pages/htmls/login.html', {'user_not_exists': False, 'password_not_match': False, 'logged_in': True, 'user': request.user})
            else:
                return render(request, 'pages/htmls/login.html', {'user_not_exists': False, 'password_not_match': True, 'logged_in': False})
        else:
            return render(request, 'pages/htmls/login.html', {'user_not_exists': True, 'password_not_match': False, 'logged_in': False})
    else:
        return render(request, 'pages/htmls/login.html', {'user_not_exists': False, 'password_not_match': False, 'logged_in': False})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home')

def add_comment(request, post_id):
    comments = Comment.objects.all()
    current_post = Post.objects.get(id=post_id)
    current_user = request.user
    if request.method == 'POST':
        content = str(request.POST.get('comment_content'))
        sender_id = current_user.id
        if current_user.first_name == '' and current_user.last_name == '':
            sender_name = current_user.username
        else:
            sender_name = f"{current_user.first_name} {current_user.last_name}"
        comment = Comment(post=current_post, content=content, sender_id=sender_id, sender_name=sender_name)
        comment.save()
        return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments})
    else:
        return render(request, 'posts/view_post.html', {'post': current_post, 'comments': comments})
    
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    comment.delete()
    return render(request, 'posts/view_post.html', {'post': post, 'comments': Comment.objects.all()})

def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = comment.post
    if request.method == 'POST':
        content = str(request.POST.get('comment_content'))
        comment.content = content
        comment.save()
        return render(request, 'posts/view_post.html', {'post': post, 'comments': Comment.objects.all()})
    else:
        return render(request, 'posts/edit_comment.html', {'comment': comment, 'user': request.user })