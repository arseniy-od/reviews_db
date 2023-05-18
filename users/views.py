from django.shortcuts import render
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from .models import MyTitlesUser as User


class SendConfirmationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = self.request.data["email"]
        password = create_password()
        send_email(email, password)
        User.objects.create_user(email, password)
        return Response({"result": "Check your email"}, status=status.HTTP_200_OK)


def send_email(email, text):
    send_mail(
        'Your confirmaution code',
        f'Use this code to authorize: \n{text}',
        'from@example.com',
        [email],
        fail_silently=False,
    )


def create_password():
    password = User.objects.make_random_password()
    return password
