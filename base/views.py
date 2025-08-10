from django.shortcuts import render
from .models import Room
from .forms import RoomForm



def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        room = RoomForm(request.POST)
        if form.as_valid():
            form.save()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)