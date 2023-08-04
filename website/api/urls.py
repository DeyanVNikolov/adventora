from django.urls import path
from . import views

urlpatterns = [
    path('eik/<str:bulstat>/<str:security_code>', views.eik, name='eik'),
]