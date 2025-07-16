import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='towns')

    def __str__(self):
        return self.name


class Location(models.Model):
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='locations')
    district = models.CharField(max_length=255, blank=True)
    microdistrict = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.town.name}, St. {self.street}, house {self.house_number}"


class Building(models.Model):
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='building')
    floors_total = models.IntegerField()
    wall_material = models.CharField(max_length=100, blank=True)
    construction_year = models.PositiveIntegerField(blank=True, null=True)
    house_amenities = models.CharField(blank=True, max_length=255)
    parking = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Building at {self.location}"


class Apartment(models.Model):
    class Balcony(models.TextChoices):
        CLASSIC = 'Classic', 'Classic'
        FRENCH = 'French', 'French'
        EXTENDED = 'Extended', 'Extended'
        LOGGIA = 'Loggia', 'Loggia'

    class Sale(models.TextChoices):
        ALTERNATIVE = 'Alternative', 'Alternative Sale'
        OPEN = 'Open', 'Open Sale'
        CONDITION = 'Condition', 'Conditional Sale'

    class Condition(models.TextChoices):
        NEW = 'New', 'New'
        ALMOST = 'Almost', 'Almost New'
        GOOD = 'Good', 'Good'
        FAIR = 'Fair', 'Fair'
        RENOVATION = 'Renovation', 'Needs Renovation'
        UNINHABITABLE = 'Uninhabitable', 'Uninhabitable'

    class Ownership(models.TextChoices):
        STATE = 'State', 'State Owned'
        PRIVATE = 'Private', 'Private'
        SHARED = 'Shared', 'Shared Ownership'
        JOINT = 'Joint', 'Joint Ownership'
        COLLECTIVE = 'Collective', 'Collective Ownership'
        FOREIGN = 'Foreign', 'Foreign'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(default='Buy Apartment')
    price = models.FloatField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='apartments')
    total_area = models.FloatField()
    living_area = models.FloatField()
    kitchen_area = models.FloatField(blank=True, null=True)
    balcony_area = models.FloatField(blank=True, null=True)
    balcony = models.BooleanField()
    balcony_type = models.CharField(choices=Balcony.choices, blank=True, null=True, default=None)
    room_count = models.IntegerField()
    description = models.TextField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="apartments")
    floor = models.IntegerField()
    sale_conditions = models.CharField(choices=Sale.choices, default=Sale.OPEN, max_length=20)
    bathroom_count = models.IntegerField(blank=True, null=True)
    ceiling_height = models.FloatField(blank=True, null=True)
    renovation = models.CharField(max_length=100, blank=True)
    condition = models.CharField(choices=Condition.choices, blank=True, default=Condition.NEW, max_length=20)
    contract_number = models.CharField(blank=True, max_length=255)
    contract_date = models.DateTimeField(blank=True, null=True)
    level_count = models.IntegerField(blank=True, null=True)
    ownership_type = models.CharField(choices=Ownership.choices, blank=True, default=Ownership.PRIVATE, max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('apartments:flat_detail', args=[str(self.id)])


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="apartments_images/")
