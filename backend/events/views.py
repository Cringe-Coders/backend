from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


# class BaseView(APIView):
#     permission_classes = IsAuthenticated
#
#     def get(self, request):
#         return Response({"Denis": "IDI NAXYI"})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def baseview(request):
    return Response({"Denis": "IDI NAXYI"})
