from django import urls
from django.urls import path
from .views import *


urlpatterns = [
    
    path('api/signup/',SignUpAPI.as_view()),
    path('api/login/',LoginAPI.as_view()),
    path('api/event/',EventAPI.as_view())
    
]
