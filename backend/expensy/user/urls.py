from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('signin/', SignIn.as_view(), name='signin'),
    path("auth/google/", GoogleLoginView.as_view()),
]
