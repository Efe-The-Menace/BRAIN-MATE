from django.shortcuts import render
from django.http import HttpResponse


rooms = [
    {
        'id': 1,
        'name': "Let's Learn python",
    },
    {
        'id': 2,
        'name': "Future of Backend Development",
    },
    {
        'id': 3,
        'name': "Evolution of C++",
    },
    {
        'id': 4,
        'name': "Ai vs Dev",
    }
]


def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, id):
    room = None
    for i in rooms:
        if i['id'] == id:
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)