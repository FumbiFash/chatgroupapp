from django.forms import ModelForm
from .models import Room, Topic, Messages,User
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username",'email','avatar']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        exclude = ["host","participants"]

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]

class MessageForm(ModelForm):
    class Meta:
        model = Messages
        fields = "__all__"

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','avatar']