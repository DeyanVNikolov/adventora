from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-hotel/', views.register_hotel, name='register-hotel'),
    path('confirm-address/', views.confirm_address, name='confirm-address'),
    path('dashboard/<hotel_id>/', views.hotel, name='hotel'),
    path('dashboard/<hotel_id>/rooms/', views.rooms, name='edit-hotel'),
    path('dashboard/<hotel_id>/rooms/add/', views.add_room, name='add-room'),
    path('dashboard/<hotel_id>/rooms/<room_id>/', views.room, name='room'),

]