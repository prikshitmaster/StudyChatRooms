from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import message
from django.db.models import Q
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from base.form import RoomModel, TopicForm
from base.models import Room, Message, Topic


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topic = Topic.objects.all()

    room_message = Message.objects.filter(Q(room__name__icontains=q))
    context = {'rooms': rooms, 'topic': topic ,'room_message':room_message}
    return render(request, 'base/mainpage/home.html', context)


def room(request, pk):
    rooms = Room.objects.get(id=pk)
    room_message = Message.objects.all().order_by('-created')
    participtant = rooms.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=rooms,
            body=request.POST.get('comment')
        )


        return redirect('room', pk=rooms.id)

    context = {'room': rooms, 'room_message': room_message, 'participtant': participtant}
    return render(request, 'base/mainpage/room.html', context)


@login_required(login_url='loginpage')
def createroom(request):
    form = RoomModel()
    context = {'form': form}
    if request.method == 'POST':
        form = RoomModel(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/room/room_create.html', context)


@login_required(login_url='loginpage')
def updateroom(request, pk):
    roomer = Room.objects.get(id=pk)
    forms = RoomModel(instance=roomer)
    if request.method == 'POST':
        form = RoomModel(request.POST, instance=roomer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': forms}
    return render(request, 'base/room/room_create.html', context)


@login_required(login_url='loginpage')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/mainpage/delete_room.html', context)


@login_required(login_url='loginpage')
def createtopic(request):
    topicform = TopicForm()
    context = {'form': topicform}
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            room =   form.save(commit=False)
            room.host ==request.user
            room.save()
            return redirect('home')
    return render(request, 'base/mainpage/add_topic.html', context)


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            message.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'base/mainpage/login_page.html')


def userProfile(request, pk):
    user =User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message = user.message_set.all()
    topic = Topic.objects.all()
    context = {'rooms' : rooms , 'room_message':room_message , 'topic':topic}
    return render(request,'base/mainpage/profile.html' ,context)

def logoutpage(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form)
            return redirect('loginpage')

    else:
        form = UserCreationForm()
    return render(request, 'base/mainpage/register.html', {'form': form})

@login_required(login_url='loginpage')
def deletemessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse(" you are not allowed")
    if request.method =='POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/mainpage/delete_room.html', {'obj': message})
