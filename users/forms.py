from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AuthenticationForm,
)

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ["email", "password"]


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class CustomUserAuthenticationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ["email", "password"]
