from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomUserAuthenticationForm
from users.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "main/home.html")
    
def signup(request):
    if request.method == 'GET':
        # show sign up form
        return render(request, 'main/signup.html', {'form':CustomUserCreationForm()})
    else:
        # validate data
        try:
        # add a new user
            user = CustomUser.objects.create_user(email=request.POST.get('email'), password=request.POST.get('password'))
            user.save()
            login(request, user)
            return redirect('home')
        except IntegrityError:
            # account with that email already exists
            return render(request, 'main/signup.html', {'form':CustomUserCreationForm(), 'error':'Account with that email already exists.'})

def signin(request):
    if request.method == 'GET':
        # show sign in form
        return render(request, 'main/signin.html', {'form':CustomUserAuthenticationForm()})
    else:
        # validate data
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user is None:
            # no user found
            return render(request, 'main/signin.html', {'form':CustomUserAuthenticationForm(), 'error':'Username or password is wrong.'})
        else:
            # data is correct
            login(request, user)
            return redirect('home')

@login_required
def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')