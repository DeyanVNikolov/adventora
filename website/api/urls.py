from django.urls import path
from . import views

urlpatterns = [
    path('eik/<str:bulstat>', views.eik, name='eik'),
]