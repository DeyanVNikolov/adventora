from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('register-hotel/', views.register_hotel, name='register-hotel'),
    path('confirm-address/', views.confirm_address, name='confirm-address'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/info/', views.edit_hotel, name='edit-hotel'),
    path('dashboard/<hotel_id>/rooms/<room_id>/', views.room, name='room'),
    path('dashboard/<hotel_id>/rooms/add/', views.add_room, name='add-room'),


]