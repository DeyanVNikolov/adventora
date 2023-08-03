from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-in', views.login, name='login'),
    path('logout', views.log_out, name='logout'),
]