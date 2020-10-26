from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from users.forms import CustomUserCreationForm, CustomUserAuthenticationForm
from users.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from scripts.solvro_city import SolvroCity
import json


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

def stops(request):
    solvro = SolvroCity('scripts/solvro_city.json')
    return render(request, "main/stops.html", {'stops':solvro.get_all_stops()})

def stops_api(request):
    solvro = SolvroCity('scripts/solvro_city.json')
    return HttpResponse(json.dumps(solvro.get_all_stops()), content_type='application/json')

def shortest_route_api(request):
    solvro = SolvroCity('scripts/solvro_city.json')
    
    try:
        # validate GET parameters
        source = request.GET.get('source')
        target = request.GET.get('target')
        
        # check if stops exists
        solvro.get_stop_id(source)
        solvro.get_stop_id(target)
        
        # return json
        return HttpResponse(json.dumps(solvro.get_shortest_route(source, target)), content_type='application/json')
    except ValueError:
        return HttpResponseBadRequest()