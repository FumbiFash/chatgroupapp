from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from . import views




urlpatterns = [
    path("login/",views.loginpg, name ="login"),
    path("logout/", views.logoutUser, name ="logout"),
    path("register/",views.registerPage, name = "register"),
    path("",views.homepg, name = "home"),
    path("room/<str:pk>/",views.room, name = "room"),
    path("newp/",views.newpg),
    path("create-room/",views.createRoom, name = "create-room"),
    path("create-topic/",views.createTopic, name = "create-topic"),
    path("update-room/<str:pk>/", views.updateRoom, name = "update-room"),
    path("delete-room/<str:pk>/", views.deleteRoom, name = "delete-room"),
    path("delete-message/<str:pk>/", views.deleteMessage, name = "delete-message"),
    path("edit-message/<str:pk>/", views.editMessage, name = "edit-message"),
    path("profile-page/<str:pk>/", views.userProfile, name = "profile-page"),
    path("update-user/", views.updateUser, name = "update-user"),
    path("topics/", views.topicsPage, name = "topics-page"),
    path("activities/", views.activityPage, name = "activity-page")




]

