from django import forms
from .models import *


class AddApartmentForm(forms.ModelForm):
    region = forms.ModelChoiceField(Region.objects.all(), label='Region')
    town_name = forms.CharField(max_length=255, label='City')

    district = forms.CharField(max_length=255, required=False, label='District')
    microdistrict = forms.CharField(max_length=255, required=False, label='Microdistrict')
    street = forms.CharField(max_length=255, label='Street')
    house_number = forms.CharField(max_length=255, label='House Number')
    latitude = forms.FloatField(required=False, label='Latitude')
    longitude = forms.FloatField(required=False, label='Longitude')

    floors_total = forms.IntegerField(required=False, label='Total Floors')
    wall_material = forms.CharField(max_length=100, required=False, label='Wall Material')
    construction_year = forms.IntegerField(required=False, label='Construction Year')
    house_amenities = forms.CharField(max_length=255, required=False, label='House Amenities')
    parking = forms.CharField(max_length=255, required=False, label='Parking')

    class Meta:
        model = Apartment
        exclude = ['owner', 'building']

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')
        town_name = cleaned_data.get('town_name')

        if not region:
            self.add_error('region', 'Region is required.')
        if not town_name:
            self.add_error('town_name', 'City is required.')

        if region and town_name:
            try:
                town_obj, created = Town.objects.get_or_create(name=town_name.strip(), region=region)
                cleaned_data['town_obj'] = town_obj
            except Exception as e:
                self.add_error('town_name', f'Error retrieving city: {e}')

        return cleaned_data

    def save(self, commit=True, owner=None):
        apartment = super().save(commit=False)

        town = self.cleaned_data['town_obj']
        district = self.cleaned_data.get('district', '')
        microdistrict = self.cleaned_data.get('microdistrict', '')
        street = self.cleaned_data.get('street')
        house_number = self.cleaned_data.get('house_number')
        latitude = self.cleaned_data.get('latitude')
        longitude = self.cleaned_data.get('longitude')

        location, loc_created = Location.objects.get_or_create(
            town=town,
            district=district,
            microdistrict=microdistrict,
            street=street,
            house_number=house_number,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
            }
        )

        if not loc_created:
            changed = False
            if latitude is not None and location.latitude != latitude:
                location.latitude = latitude
                changed = True
            if longitude is not None and location.longitude != longitude:
                location.longitude = longitude
                changed = True
            if changed:
                location.save()

        floors_total = self.cleaned_data.get('floors_total')
        wall_material = self.cleaned_data.get('wall_material', '')
        construction_year = self.cleaned_data.get('construction_year')
        house_amenities = self.cleaned_data.get('house_amenities', '')
        parking = self.cleaned_data.get('parking', '')

        building, building_created = Building.objects.get_or_create(
            location=location,
            defaults={
                'floors_total': floors_total or 0,
                'wall_material': wall_material,
                'construction_year': construction_year,
                'house_amenities': house_amenities,
                'parking': parking,
            }
        )

        if not building_created:
            changed = False
            if floors_total is not None and building.floors_total != floors_total:
                building.floors_total = floors_total
                changed = True
            if wall_material != building.wall_material:
                building.wall_material = wall_material
                changed = True
            if construction_year != building.construction_year:
                building.construction_year = construction_year
                changed = True
            if house_amenities != building.house_amenities:
                building.house_amenities = house_amenities
                changed = True
            if parking != building.parking:
                building.parking = parking
                changed = True
            if changed:
                building.save()

        apartment.building = building
        if owner:
            apartment.owner = owner

        if commit:
            apartment.save()

        return apartment
