from django.urls import path
from .views import Create, Read, NewOrder, Test

urlpatterns = [
    path('form_order/', NewOrder.as_view()),
    path('get/<str:model_name>/', Read.as_view()),
    path('create/<str:model_name>/', Create.as_view()),
    path('test_view/', Test.as_view())
]
