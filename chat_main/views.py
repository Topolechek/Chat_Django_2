from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Room, Msg


# Create your views here.

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms':rooms})

def optional(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'optional.html')
    if request.method == 'GET':
        return render(request, 'optional.html')

def room(request, room):
    username = User.username #request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_name': room_details
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.user.username
    send_msg = '#send_msg'
    if Room.objects.filter(name=room).exists():
        return redirect('/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Msg.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Сообщение успешно отправлено')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Msg.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


#auth

def reg(request):
    if request.method == 'GET':
        return render(request, 'reg.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('/ch')
            except IntegrityError:
                return render(request, 'reg.html', {'form': UserCreationForm(), 'error': "Это имя уже занято."})
        else:
            return render(request, 'reg.html', {'form':UserCreationForm(), 'error': "Пароли не совпадают."})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is None:
            return render(request, 'loginuser.html', {'form': AuthenticationForm(), 'error':'Логин и пароль не совпадают'})
        else:
            login(request, user)
            return redirect('/ch')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginuser.html')