from django.shortcuts import render
from rest_framework import viewsets
from .models import Board, BoardMessage
from .serializers import BoardSerializer, BoardMessageSerializer

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardMessageViewSet(viewsets.ModelViewSet):
    queryset = BoardMessage.objects.all()
    serializer_class = BoardMessageSerializer

# Create your views here.
