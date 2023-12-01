from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('register-hotel/', views.register_hotel, name='register-hotel'),
    path('confirm-address/', views.confirm_address, name='confirm-address'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/info/', views.edit_hotel, name='edit-hotel'),
    path('dashboard/photos/', views.photos, name='photos'),
    path('dashboard/<hotel_id>/deletephoto/<photo_id>/', views.deletephoto, name='deletephoto'),
    path('dashboard/<hotel_id>/add-reservation/', views.add_reservation, name='add-reservation'),
    path('dashboard/<hotel_id>/rooms/add/', views.add_room, name='add-room'),
    path('dashboard/<hotel_id>/rooms/<room_id>/', views.room, name='room'),
    path('dashboard/<hotel_id>/rooms/<room_id>/delete/', views.deleteroom, name='delete-room'),
    path('dashboard/<hotel_id>/rooms/<room_id>/updatestatus/<status>/', views.updateroomstatus, name='updateroomstatus'),
    path('dashboard/<hotel_id>/rooms/<room_id>/occupy/', views.occupy, name='occupyroom'),
    path('dashboard/<hotel_id>/rooms/<room_id>/occupy/<reservationid>', views.occupyreversed, name='occupyreversed'),



]