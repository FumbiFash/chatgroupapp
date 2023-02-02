from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room, Messages,Topic,User
from .forms import RoomForm, TopicForm, MessageForm,UserForm,MyUserCreationForm
# from django.contrib.auth.models import User

from django.db.models import Q

# Create your views here.



def loginpg(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        #try:
            #user = User.objects.get(username=username)

        #except:
            #messages.error(request,"user does not exist")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "username/password does not exist")

    
    context = {"page":page}
    return render(request,"login_register.html",context)

def logoutUser(request):
    logout(request)
    return redirect("home")

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect("home")
        else:
            messages.error(request,"Error in registration")
    context = {"form":form}

    return render(request,"login_register.html",context)

def homepg(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""



    rooms = Room.objects.filter(Q(topic__name__icontains=q)
                                |Q(name__icontains = q)
                                |Q(description__icontains = q))

    rooms_count = rooms.count()
    room_messages = Messages.objects.filter(Q(topic__name__icontains=q)
                                            |Q(room__name__icontains=q))
    # OR YOU COULD DO ' room_messages = Messages.objects.filter(Q(room__topic__name__icontains = q)) ',
    # Rather than adding topic object to Messages. But good practice.
    topic = Topic.objects.all()[0:3]
    context = {"rooms":rooms, "topic": topic,"rooms_count":rooms_count,"room_messages":room_messages}
    return render(request,"home.html", context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_message = room.messages_set.all().order_by("-created")
    # _set.all allows to access reverse relations on a model
    participants = room.participants.all()
    if request.method == "POST":
        message = Messages.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get("body"),
        topic = room.topic
        )
        room.participants.add(request.user)
        return redirect("room", pk = room.id)


    topic = Topic.objects.all()
    context = {"room":room, "topic":topic,"room_message":room_message,"participants":participants}

    return render(request,"room.html",context)

def newpg (request):
    messages = Messages.objects.filter()[:1].get()
    return render(request, "rest.html", {"messages":messages})



@login_required(login_url="login")
def createRoom(request):
    topics = Topic.objects.all()
    form = RoomForm()

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get("name"),
            description = request.POST.get("description")
        )
        return redirect("home")


    context = {"form":form,"topics":topics}
    return render(request,"create-room.html",context)


def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm( instance = room)

    if request.user != room.host:

        return HttpResponse("you are not the user")

    if request.method == "POST":

        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name = topic_name)

        room.host = request.user
        room.topic = topic
        room.name = request.POST.get("name")
        room.description = request.POST.get("description")
        room.save()
        return redirect("home")


    context = {"form":form,"topics":topics,"room":room}
    return render (request, "create-room.html",context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("you are not the user")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"room":room}
    return render(request,"delete-room.html",context)

def deleteMessage(request,pk):
    message = Messages.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("you are not the user")
    if request.method == "POST":
        message.delete()

        return redirect("home")
    context = {"message":message}
    return render(request,"delete-message.html",context)

@login_required(login_url="login")
def editMessage(request,pk):
    message = Messages.objects.get(id=pk)
    form = MessageForm(instance = message)

    if request.method == "POST":
        form = MessageForm(request.POST,instance = message)
        form.save()
    return render(request,"edit-message.html",{"form":form})



def createTopic(request):
    form = TopicForm()

    if request.method == "POST":
        print(request.POST.get("name"))

    context = {"form": form}
    return render(request, "create-topic.html", context)

def userProfile(request,pk):

    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topic = Topic.objects.all()
    room_messages = Messages.objects.all()
    context = {"user":user,"rooms":rooms,"room_messages":room_messages,"topic":topic}
    return render(request, "profile-page.html",context)

@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)

        if form.is_valid():
            form.save()

            return redirect("profile-page",pk = user.id)


    context = {"form":form}
    return render(request, "update-user.html",context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    context = {"topics":topics}
    return render(request, "topics.html",context)

def activityPage(request):
    room_messages = Messages.objects.all()
    context = {"room_messages":room_messages}
    return render(request, "activity.html",context)