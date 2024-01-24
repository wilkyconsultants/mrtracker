# serializers.py

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class TagListSerializer(serializers.Serializer):
    option = serializers.CharField()
    user_id = serializers.CharField()

class TagMapSerializer(serializers.Serializer):
    ser = serializers.CharField()
    username = serializers.CharField()
    date = serializers.CharField()
    days = serializers.IntegerField()

class ChartSerializer(serializers.Serializer):
    serialNumber = serializers.CharField()
    username = serializers.CharField()
    days = serializers.IntegerField()
