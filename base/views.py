from django.contrib import messages
from django.shortcuts import render , redirect
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room , Topic , Message , User
from .forms import RoomForm , UserForm , MyUserCreationForm
from django.http import HttpResponse


# from django.http import HttpResponse


# rooms = [
#     {'id':1 , 'name' :'lets learn  python ! '},
#     {'id':2 , 'name' :'design with me  '},
#     {'id':3 , 'name' :'frontend developer '},
# ]

def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q))
    
    room_count = rooms.count()
    Topics = Topic.objects.all()
    room_message = Message.objects.filter(Q(room__topic__name__icontains=q))
    content={'rooms':rooms,'Topics':Topics,'room_count':room_count,'room_message':room_message}
    return render(request,'base/home.html',content)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room ,
            body=request.POST.get('body')
            )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context = {'room':room,'room_message':room_message,'participants':participants}
    return render(request,'base/room.html',context)




@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic = topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.user:
        return HttpResponse('You do not own this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic = topic
        room.name=request.POST.get('name')        
        room.description=request.POST.get('description')
        room.save()
        return redirect("home")
    
    context={'form':form,'topics':topics ,'room':room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You do not own this room')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def loginpage(request):
    page ="login"

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user = authenticate(request, username=username , password=password )
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page':page}
    return render(request,'base/login_register.html',context)

def logoutuser(request):
    logout(request)
    return redirect('home')




@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here !!! ')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_message= user.message_set.all()
    Topics = Topic.objects.all()
    context={'user':user, 'rooms':rooms ,'room_message':room_message , 'Topics':Topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    form=UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
        return redirect('user_profile',pk=user.id)
    context={'form':form}
    return render(request,'base/update-user.html',context)

# def registerpage(request):
#     form = MyUserCreationForm()
#     if request.method == 'POST':
#         form = MyUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user = form.save()
#             login(request, user)  # Automatically log the user in after registration
#             return redirect('home')
#         else:
#             messages.error(request, 'an error accuse you registration')
#     return render(request,'base/login_register.html',{'form':form})

def registerpage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')
    return render(request, 'base/login_register.html', {'form': form})
