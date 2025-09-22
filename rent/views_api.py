from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from apartments.permissions import IsOwnerOrAdmin
from apartments.serializers import TownSerializer, LocationSerializer, RegionSerializer

from .models import *
from .serializers import *


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RentCreateSerializer
        return RentSerializer

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