from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('hotels/', views.hotels, name='hotels'),
    path('hotels/<hotel_id>/', views.hotel, name='hotel'),
    path('room/<room_id>/', views.room, name='room'),


    path('invoice/<reservation_id>/', views.invoicesserve, name='invoicesserve'),



    path('contacts/', views.contacts, name='contacts'),
    path('privacy/', views.privacy, name='privacy'),
    path('partnerships/', views.partnerships, name='partnerships'),
    path('security-check/', views.security_check, name='security-check'),
    path('emergency-in-bg/', views.emergency_in_bg, name='emergency-in-bg'),
    path('stranded-abroad/', views.stranded_abroad, name='stranded-abroad'),

]

handler404 = 'home.views.handle404'
handler500 = 'home.views.handle500'
