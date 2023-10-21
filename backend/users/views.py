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
        username = user_data.get("email")
        password = user_data.get("password")
        try:
            first_name = user_data.get("first_name")
            last_name = user_data.get("last_name")
        except Exception as e:
            return Response({"status": "400", "error": "no first/last name", "server_error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get_or_none(username=username)
        if user is None:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.email = username
            user.save()
            return Response({"status": "200"}, status=status.HTTP_200_OK)
        return Response({"status": "500", "error": "user already created"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileAPIView(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        if user is not None:
            return Response(serializers.UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"status": "404"}, status=status.HTTP_404_NOT_FOUND)


class ProfileAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request: Request):
        user = User.objects.get_or_none(pk=request.user.id)
        # user = User.objects.get_or_none(pk=1)
        if user is not None:
            return Response(serializers.UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"status": "404"}, status=status.HTTP_404_NOT_FOUND)


class ProfileUpdateAPIView(APIView):
    # permission_classes = (IsAuthenticated, )

    # def post(self, request: Request):
    #     user = User.objects.get_or_none(pk=request.user.pk)
    #     if user is not None:
    #         pass
    #     return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        user = User.objects.get_or_none(pk=request.user.id)
        # user = User.objects.get_or_none(pk=1)
        if user is not None:
            serializer = serializers.UserProfileUpdate(data=request.data, instance=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "200"}, status=status.HTTP_200_OK)
        return Response({"status": "404", "error": "User not authorized"}, status=status.HTTP_404_NOT_FOUND)
