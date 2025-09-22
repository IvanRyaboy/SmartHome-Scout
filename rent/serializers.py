from rest_framework import serializers
from apartments.serializers import BuildingSerializer, BuildingCreateSerializer
from apartments.models import Region, Town, Location
from .models import *


class RentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentImage
        fields = ['id', 'image']


class RentSerializer(serializers.ModelSerializer):
    images = RentImageSerializer(many=True, read_only=True)
    building = BuildingSerializer(read_only=True)
    building_id = serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(),
        source='building',
        write_only=True
    )

    class Meta:
        model = Rent
        fields = '__all__'


class RentCreateSerializer(serializers.ModelSerializer):
    building = BuildingCreateSerializer()
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Rent
        exclude = ['owner', 'id']

    def create(self, validated_data):
        user_model = get_user_model()
        user = user_model.objects.get(id='736166cf-991f-4057-a8f6-ebdd1eee55e2')

        building_data = validated_data.pop('building')
        location_data = building_data.pop('location')
        town_data = location_data.pop('town')
        region_data = town_data.pop('region')
        images = validated_data.pop('images', [])

        region = Region.objects.get_or_create(**region_data)

        town = Town.objects.get_or_create(region=region, **town_data)

        location = Location.objects.get_or_create(town=town, **location_data)

        building = Building.objects.get_or_create(location=location, **building_data)

        apartment = Rent.objects.create(
            building=building,
            owner=user,
            **validated_data
        )

        for image in images:
            RentImage.objects.create(apartment=apartment, image=image)

        return apartment

