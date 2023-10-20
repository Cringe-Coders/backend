import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from users.models import User

from . import serializers


class SignUpView(APIView):
    def post(self, request: Request):
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")
        user = User.objects.get_or_none(username=username)
        if user is None:
            user = User.objects.create_user(username=username, password=password)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user is not None:
            return Response(serializers.UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request):
        user = User.objects.get(pk=request.user.pk)
        if user is not None:
            return Response(serializers.UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request):
        pass
