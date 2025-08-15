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


class TownCreateSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Town
        fields = '__all__'


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


class LocationCreateSerializer(serializers.ModelSerializer):
    town = TownCreateSerializer()

    class Meta:
        model = Location
        fields = '__all__'


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


class BuildingCreateSerializer(serializers.ModelSerializer):
    location = LocationCreateSerializer()

    class Meta:
        model = Building
        fields = '__all__'


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
    building = BuildingCreateSerializer()
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Apartment
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

        apartment = Apartment.objects.create(
            building=building,
            owner=user,
            **validated_data
        )

        for image in images:
            ApartmentImage.objects.create(apartment=apartment, image=image)

        return apartment

