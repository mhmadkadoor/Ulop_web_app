from django.shortcuts import render
from posts.models import Post
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
def home (request):
    return render(request, 'pages/htmls/home.html', {'posts': Post.objects.all(), 'user': request.user})
def about (request):
    return render(request, 'pages/htmls/about.html')
def courses (request):
    return render(request, 'pages/htmls/courses.html')

@login_required(login_url='login')
def profile (request):
    current_user = request.user
    if request.method == 'POST':
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
        
    return render(request, 'pages/htmls/profile.html', {'posts': Post.objects.all(),'user': current_user , 'UserS': User.objects.all()})

def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if str(password) != str(confirm_password):
            print(f"Password: {password} Confirm Password: {confirm_password}")
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
                user = User.objects.create_user(username=username, password=password)
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