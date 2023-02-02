from django.db import models
from django.contrib.auth.models import User, AbstractUser


class User(AbstractUser):

    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(null=True,unique=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True,default="favicon.ico")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Topic(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=200)
    period = models.CharField(max_length=200,null=True)
    description = models.TextField(null=True, blank = True)
    participants = models.ManyToManyField(User, related_name="participants", blank = True)
    updated = models.DateTimeField (auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.name

class Messages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="1")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE, null = True)


    class Meta:
        ordering = ["-updated"]
    def __str__(self):
        return self.body

