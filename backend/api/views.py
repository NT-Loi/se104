from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *

# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class SachListCreate(generics.ListCreateAPIView):
    queryset = Sach.objects.all()
    serializer_class = SachSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))

class SachDelete(generics.DestroyAPIView):
    queryset = Sach.objects.all()
    serializer_class = SachSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]