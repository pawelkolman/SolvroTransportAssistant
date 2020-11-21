from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from users.models import CustomUser
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class SignUp(View):
    template_name = "users/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # validate data
        try:
            # validate email
            validate_email(request.POST.get("email"))

            # add a new user
            user = CustomUser.objects.create_user(
                email=request.POST.get("email"),
                password=request.POST.get("password"),
            )
            user.save()
            login(request, user)
            return redirect("home")

        except IntegrityError:
            # account with that email already exists
            return render(
                request,
                self.template_name,
                {"error": "Account with that email already exists."},
            )

        except ValidationError:
            # invalid data
            return render(
                request, self.template_name, {"error": "Wrong data provided."}
            )


class SignIn(View):
    template_name = "users/signin.html"

    def get(self, request):
        # show sign in form
        return render(request, self.template_name)

    def post(self, request):
        # validate data
        user = authenticate(
            request,
            email=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user is None:
            # no user found
            return render(
                request,
                self.template_name,
                {"error": "Username or password is wrong."},
            )
        else:
            # data is correct
            login(request, user)
            return redirect("home")


class SignOut(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect("home")
