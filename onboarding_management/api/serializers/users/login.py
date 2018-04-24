from rest_framework import serializers


class UserLogInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
