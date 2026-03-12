from django_filters.rest_framework import DjangoFilterBackend
from pgvector.django import CosineDistance
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filters import ApartmentFilter
from .models import ListingEmbedding
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
        return [AllowAny(),]

    @action(detail=True, url_path='similar', methods=['get'])
    def similar(self, request, pk=None):
        """Return apartments with similar embedding (vector similarity)."""
        apartment = self.get_object()
        ref = ListingEmbedding.objects.filter(apartment=apartment).first()
        if not ref:
            return Response([])
        ref_vec = ref.embedding
        similar_embeddings = (
            ListingEmbedding.objects
            .filter(apartment__isnull=False)
            .exclude(apartment=apartment)
            .annotate(distance=CosineDistance('embedding', ref_vec))
            .order_by('distance')[:10]
        )
        apartment_ids = [e.apartment_id for e in similar_embeddings]
        qs = Apartment.objects.filter(pk__in=apartment_ids)
        # Preserve order by distance
        order = {aid: i for i, aid in enumerate(apartment_ids)}
        qs = sorted(qs, key=lambda a: order.get(a.pk, 999))
        serializer = ApartmentSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)


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
