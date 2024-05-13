from django.urls import path, include
from .views import Auth

urlpatterns = [
    path('auth/', Auth.as_view()),
]