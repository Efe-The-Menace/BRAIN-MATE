from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(room__name__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    all_topics = Topic.objects.all()

    room_count  = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages, 'all_topics': all_topics}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    comments = room.message_set.all()
    participants = room.participants.all()
    
    if request.method == 'POST':
        new_message = Message.objects.create(
            user =  request.user,
            room = room,
            body = request.POST.get('body')
        )
        new_message.save()
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'comments': comments, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    status = 'create'
    topics = Topic.objects.all()
    form = RoomForm()
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name=request.POST.get('name'),
            description = request.POST.get('description')

        )
        return redirect('home')
    context = {'form': form, 'status': status, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if room.host != request.user:
        return HttpResponse("You can't perform this action")
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.descriptionm =request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if room.host != request.user:
        return HttpResponse("You can't perform this action")
    context = {'obj': room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url='/')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("Hey, You can't do that!")
    room = message.room.id
    if request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted!")
        return redirect('room', room)
    return render(request, 'base/delete.html', {'obj': message})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(
        name__icontains=q
    )
    return render(request, 'base/topics.html', {'topics': topics})\
    

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})