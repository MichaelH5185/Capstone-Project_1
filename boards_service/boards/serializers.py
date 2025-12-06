from rest_framework import serializers
from .models import Board, BoardMessage

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board 
        fields = '__all__' 

class BoardMessageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Board
        fields = '__all__'
        