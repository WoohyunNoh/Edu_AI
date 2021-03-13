from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    print(room_name)
    return render(request, 'room.html', {
        'room_name': room_name
    })


def temp(request):
    pass
