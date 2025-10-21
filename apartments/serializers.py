from rest_framework import serializers
from .models import *
from django.db import transaction, IntegrityError
from django.contrib.auth import get_user_model
from accounts.utils import get_service_user


User = get_user_model()


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


class OwnerUserDefault:
    requires_context = True

    def __call__(self, serializer_field):
        ctx = serializer_field.context or {}
        req = ctx.get('request')
        if req and hasattr(req, 'user') and req.user and req.user.is_authenticated:
            return req.user
        owner = ctx.get('owner')
        if isinstance(owner, User):
            return owner
        return get_service_user()

    def __repr__(self):
        return f"{self.__class__.__name__}()"


class ApartmentCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=OwnerUserDefault())
    _id = serializers.UUIDField(required=False)
    building = BuildingCreateSerializer()
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Apartment

    @transaction.atomic
    def create(self, validated_data):
        building_data = validated_data.pop('building')
        location_data = building_data.pop('location')
        town_data = location_data.pop('town')
        region_data = town_data.pop('region')

        images = validated_data.pop('images', [])
        apt_id = validated_data.pop('_id', None)

        region, _ = Region.objects.get_or_create(name=region_data['name'])

        town, _ = Town.objects.get_or_create(region=region, name=town_data['name'])

        loc_lookup = dict(
            town=town,
            district=location_data.get('district', '') or '',
            microdistrict=location_data.get('microdistrict', '') or '',
            street=location_data.get('street') or None,
            house_number=location_data.get('house_number') or None,
        )
        loc_defaults = {}
        if 'latitude' in location_data:
            loc_defaults['latitude'] = location_data['latitude']
        if 'longitude' in location_data:
            loc_defaults['longitude'] = location_data['longitude']

        location, created_loc = Location.objects.get_or_create(**loc_lookup, defaults=loc_defaults)
        if not created_loc and loc_defaults:
            to_update = {}
            for k, v in loc_defaults.items():
                if getattr(location, k) != v:
                    to_update[k] = v
            if to_update:
                for k, v in to_update.items():
                    setattr(location, k, v)
                location.save(update_fields=list(to_update.keys()))

        b_defaults = {
            'floors_total': building_data['floors_total'],
            'wall_material': building_data.get('wall_material', '') or '',
            'construction_year': building_data.get('construction_year'),
            'house_amenities': building_data.get('house_amenities', '') or '',
            'parking': building_data.get('parking', '') or '',
        }
        building, created_b = Building.objects.update_or_create(
            location=location,
            defaults=b_defaults
        )

        apt_kwargs = dict(
            building=building,
            **validated_data
        )
        if apt_id is not None:
            apt_kwargs['id'] = apt_id

        apartment = Apartment.objects.create(**apt_kwargs)

        for img in images:
            ApartmentImage.objects.create(apartment=apartment, image=img)

        return apartment

