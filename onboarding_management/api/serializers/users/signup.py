from rest_framework import serializers

from ...models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup
    """

    class Meta:
        model = User
        fields = '__all__'
