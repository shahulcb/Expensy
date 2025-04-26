from django.urls import path
from .views import *

urlpatterns = [
    path('user-list', UserView.as_view(), name='user'),
]