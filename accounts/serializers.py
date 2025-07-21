from django.contrib.auth import get_user_model
from rest_framework import serializers
from apartments.serializers import ApartmentSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'apartments']


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username')
        )
        return user
