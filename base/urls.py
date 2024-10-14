from django.urls import path
from . import views 


urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('create_room/',views.createRoom,name='create-room'),
    path('update_room/<str:pk>/',views.updateRoom,name='update_room'),
    path('delete_room/<str:pk>/',views.deleteRoom,name='delete_room'),
    path('login/',views.loginpage,name='login'),
    path('register/',views.registerpage,name='register'),
    path('logout/',views.logoutuser,name='logout'),
    path('delete_Message/<str:pk>/',views.deleteMessage,name='delete_Message'),
    path('user_profile/<str:pk>/',views.userProfile,name='user_profile'),

]