from django.contrib import admin
from .models import Room, Topic, Messages
from .models import User
# Register your models here.



class roomAdmin(admin.ModelAdmin):
    list_display = ("id","name","description","topic","updated","period")


class messageAdmin(admin.ModelAdmin):
    list_display = ("room","body","topic")


class topicAdmin(admin.ModelAdmin):
    list_display = ("name","type")

class userAdmin(admin.ModelAdmin):
    list_display = ("email","name")

admin.site.register(User,userAdmin)
admin.site.register(Room,roomAdmin)
admin.site.register(Messages,messageAdmin)
admin.site.register(Topic,topicAdmin)