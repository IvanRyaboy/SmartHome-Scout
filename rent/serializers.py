from rest_framework import serializers
from apartments.serializers import BuildingSerializer, BuildingCreateSerializer
from apartments.models import Region, Town, Location
from .models import *
from django.contrib.auth import get_user_model
from accounts.utils import get_service_user


User = get_user_model()


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


class RentCreateSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=OwnerUserDefault())
    _id = serializers.UUIDField(required=False)
    building = BuildingCreateSerializer()
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = Rent

    def create(self, validated_data):
        building_data = validated_data.pop('building')
        location_data = building_data.pop('location')
        town_data = location_data.pop('town')
        region_data = town_data.pop('region')
        images = validated_data.pop('images', [])
        rent_id = validated_data.pop('_id', None)

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
            'parking': building_data.get('parking', '') or ''
        }
        building, created_b = Building.objects.update_or_create(
            location=location,
            defaults=b_defaults
        )

        rent_kwargs = dict(
            building=building,
            **validated_data
        )
        if rent_kwargs is not None:
            rent_kwargs['id'] = rent_id

        rent = Rent.objects.create(**rent_kwargs)

        for image in images:
            RentImage.objects.create(rent=rent, image=image)

        return rent

