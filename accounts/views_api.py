from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from accounts.serializers import UserSerializer, UserCreateSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), ]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdminUser(), ]
        else:
            return [AllowAny(), ]
