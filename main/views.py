from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from users.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from scripts.solvro_city import SolvroCity
from main.forms import FavouriteForm
import json
import re


def home(request):
    return render(request, "main/home.html")
    
def signup(request):
    if request.method == 'GET':
        # show sign up form
        return render(request, 'main/signup.html')
    else:
        # validate data
        try:
        # validate e-mail
            if not re.match(r"[^@]+@[^@]+\.[^@]+", request.POST.get('email')):
                raise ValidationError("wrong email")
        # add a new user
            user = CustomUser.objects.create_user(email=request.POST.get('email'), password=request.POST.get('password'))
            user.save()
            login(request, user)
            return redirect('home')
        except IntegrityError:
            # account with that email already exists
            return render(request, 'main/signup.html', {'error':'Account with that email already exists.'})
        except ValidationError:
            # some fucker is trying to provide wrong data
            return render(request, 'main/signup.html', {'error':'Wrong data provided.'})

def signin(request):
    if request.method == 'GET':
        # show sign in form
        return render(request, 'main/signin.html')
    else:
        # validate data
        user = authenticate(request, email=request.POST.get('email'), password=request.POST.get('password'))
        if user is None:
            # no user found
            return render(request, 'main/signin.html', {'error':'Username or password is wrong.'})
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

def shortest_route(request):
    solvro = SolvroCity('scripts/solvro_city.json')
    if request.method == 'GET':
        # show the form
        return render(request, 'main/shortest_route_form.html', {'stops':solvro.get_all_stops()})
    else:
        try:
            # validate source and target provided data
            source = request.POST.get('source')
            target = request.POST.get('target')
            
            # check if stops exists
            solvro.get_stop_id(source)
            solvro.get_stop_id(target)
            
            # return the shortest route with a distance
            return render(request, 'main/shortest_route.html', {'shortest_route':solvro.get_shortest_route(source, target), 'source':source, 'target':target})
        except ValueError:
            return render(request, 'main/shortest_route_form.html', {'error':'Wrong data provided.'})

def shortest_route_api(request):    
    try:
        solvro = SolvroCity('scripts/solvro_city.json')
        
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

@login_required
def favourites(request):
    if request.POST.get('operation') == 'add':
        # try:
            form = FavouriteForm(request.POST)
            new_favourite = form.save(commit=False) # don't save yet, because we need to change the `user` field
            new_favourite.user = request.user
            new_favourite.save()
            return redirect('home')
        # except ValueError:
            # return redirect('home')