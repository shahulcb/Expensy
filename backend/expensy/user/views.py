from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework import generics, status
from django.contrib.auth import authenticate
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.db import transaction
from django.shortcuts import get_object_or_404
import random

from .models import *
from .serializers import *
from .common_functions import *
from .tasks import send_otp_to_email
# views start here

User = get_user_model()

class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        self.user = user
        otp = str(random.randint(100000, 999999))
        otp_record, _ = UserOTP.objects.get_or_create(user=user)
        otp_record.set_otp(otp)
        send_otp_to_email.delay({
            'email': user.email,
            'otp': otp
        })

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        tokens = generate_tokens_for_user(self.user)
        response_data = {
        'status': 'success',
        'message': f'User registered. OTP sent to {self.user.email}',
        'access_token': tokens['access_token'],
        'refresh_token': tokens['refresh_token'],
        }
        return Response({'status': 'success', 'data': response_data}, status=status.HTTP_201_CREATED)
        
class VerifyOTP(APIView):
    @transaction.atomic
    def post(self, request):
        email = request.data['email']
        otp = str(request.data['otp']).strip()
        if validate_fields:=validate_required_fields(request.data, ['email', 'otp']):
            return validate_fields
        user = get_object_or_404(User, email=email)
        try:
            otp_record = UserOTP.objects.get(user=user)
        except UserOTP.DoesNotExist:
            return Response({'status': 'error', 'message': 'OTP not found for this user'},status=status.HTTP_404_NOT_FOUND)
        if otp_record.is_expired():
            return Response({'status': 'error', 'message': 'OTP expired'},status=status.HTTP_400_BAD_REQUEST)
        if not otp_record.check_otp(otp):
            return Response({'status': 'error', 'message': 'Invalid OTP'},status=status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        otp_record.delete()
        return Response({'status': 'success', 'message': 'Email verified successfully'},status=status.HTTP_200_OK)


class SignIn(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if validate_fields:=validate_required_fields(request.data, ['email', 'password']):
            return validate_fields
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'status': 'error', 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_verified:
            otp = str(random.randint(100000, 999999))
            otp_record, _ = UserOTP.objects.get_or_create(user=user)
            otp_record.set_otp(otp)
            send_otp_to_email.delay({'email': user.email,'otp': otp})
            return Response({'status': 'pending','message': 'Email not verified. OTP has been sent to your email again.'}, status=status.HTTP_403_FORBIDDEN)
        token = generate_tokens_for_user(user)
        return Response({'status': 'success','access_token': token['access_token'],'refresh_token': token['refresh_token'],}, status=status.HTTP_200_OK)

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get("token")
        try:
            id_info = id_token.verify_oauth2_token(token, google_requests.Request())
            email = id_info.get("email")
            if not email:
                return Response({'status': 'error','message': 'Invalid Google token'}, status=status.HTTP_400_BAD_REQUEST)
            user, created = User.objects.get_or_create(email=email, defaults={"is_verified": True,})
            if created:
                user.set_unusable_password()
                user.save()
            if not user.is_verified:
                user.is_verified = True
                user.save()
            tokens = generate_tokens_for_user(user)
            return Response(tokens, status=200)
        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
class HomeView(APIView):
    def get(self, request):
        return Response({'status': 'success', 'message': 'Welcome to the home page!'}, status=status.HTTP_200_OK)