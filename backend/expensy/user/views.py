from django.shortcuts import render
from rest_framework import generics

# Create your views here.
class UserView(generics.CreateAPIView):
    def get(self, request):
        pass