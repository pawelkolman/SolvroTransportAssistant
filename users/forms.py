from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
        fields = ('email',)