from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .users import Admin
# Create your views here.

class Auth(APIView):
    def post(self, request):
        new_token = Admin().authentificate(request.data['login'], request.data['password'])
        print(new_token)
        return Response({'token': new_token})
    