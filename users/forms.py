from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

class UserRegisterform(UserCreationForm):
    email = models.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2' ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']