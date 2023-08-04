from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('logout', views.log_out, name='logout'),
]