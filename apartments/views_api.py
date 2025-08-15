from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import permissions
from rest_framework.response import Response

from .filters import ApartmentFilter
from .models import *
from .permissions import IsOwnerOrAdmin
from .serializers import *


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ApartmentCreateSerializer
        return ApartmentSerializer

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(),]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin(),]
        else:
            return [AllowAny(),]


class TownViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TownSerializer
    queryset = Town.objects.all()


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class BuildingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
