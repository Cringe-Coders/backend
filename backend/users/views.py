import json

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


from users.models import User


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
