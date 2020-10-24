from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    password1 = None
    password2 = None
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'password']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'password']


class CustomUserAuthenticationForm(UserCreationForm):
    password1 = None
    password2 = None
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['email', 'password']