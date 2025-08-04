from rest_framework import serializers
from .models import *


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = "__all__"


class TownSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    region_id = serializers.PrimaryKeyRelatedField(
        queryset=Region.objects.all(),
        source='region',
        write_only=True
    )

    class Meta:
        model = Town
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    town = TownSerializer(read_only=True)
    town_id = serializers.PrimaryKeyRelatedField(
        queryset=Town.objects.all(),
        source='town',
        write_only=True
    )

    class Meta:
        model = Location
        fields = "__all__"


class BuildingSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(),
        source='location',
        write_only=True
    )

    class Meta:
        model = Building
        fields = "__all__"


class ApartmentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentImage
        fields = ['id', 'image']


class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImageSerializer(many=True, read_only=True)
    building = BuildingSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(),
        source='building',
        write_only=True
    )

    class Meta:
        model = Apartment
        fields = '__all__'


class ApartmentCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Apartment
        fields = ['id', 'title', 'price', 'building', 'total_area', 'living_area',
                  'kitchen_area', 'balcony_area', 'balcony',
                  'room_count', 'description', 'floor', 'sale_conditions',
                  'bathroom_count', 'ceiling_height', 'renovation', 'condition',
                  'contract_number', 'contract_date', 'level_count', 'ownership_type',
                  'images']

    def create(self, validated_data):
        apartment = Apartment.objects.create(**validated_data)

        request = self.context.get('request')
        if request and hasattr(request, 'FILES'):
            images = request.FILES.getlist('images')

            for image in images:
                ApartmentImage.objects.create(apartment=apartment, image=image)
        return apartment

