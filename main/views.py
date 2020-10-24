from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate


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
            user = CustomUser.objects.create_user(email=request.POST['email'], password=request.POST['password'])
            user.save()
            login(request, user)
            return redirect('home')
        except IntegrityError:
            # account with that email already exists
            return render(request, 'main/signup.html', {'form':CustomUserCreationForm(), 'error':'Account with that email already exists.'})

def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')