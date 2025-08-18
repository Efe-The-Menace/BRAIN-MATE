from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterform, UserForm
from django.contrib.auth.decorators import login_required
from base.models import Topic

# Create your views here.


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Username or Password')

    context = {'page': page}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')


def registerUser(request):
    form = UserRegisterform()
    if request.method == 'POST':
        form = UserRegisterform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "You have sucessfully registered! Login to continue.")
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    context = {'form': form}
    return render(request, 'users/login_register.html', context)

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'users/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
        user = request.user
        form = UserForm(instance=user)
        if request.method == 'POST':
            form = UserForm(request.POST, instance=user)
            form.save()
            return redirect('profile', pk=user.id)
        return render(request, 'users/update-user.html', {'form': form})