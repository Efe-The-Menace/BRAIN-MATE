from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.forms import ModelForm

class UserRegisterform(UserCreationForm):

    class Meta:
        model = User
        fields = ['name','username', 'email', 'password1', 'password2' ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'avatar']