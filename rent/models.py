import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from apartments.models import Building


class Rent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    title = models.CharField(default='Rent apartments')
    price = models.FloatField()
    total_area = models.FloatField()
    living_area = models.FloatField()
    kitchen_area = models.FloatField(blank=True, null=True)
    balcony = models.BooleanField(default=False)
    floor = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rents')
    room_count = models.PositiveIntegerField(blank=True, null=True)
    separate_rooms = models.PositiveIntegerField(blank=True, null=True)
    renovation = models.CharField(max_length=100, blank=True, null=True)
    furniture = models.BooleanField(default=True)
    bathroom = models.CharField(max_length=100, blank=True, null=True)
    quarter = models.FloatField(blank=True, null=True)
    term_of_rent = models.CharField(max_length=100, blank=True, null=True)
    contract_number = models.CharField(max_length=100, blank=True, null=True)
    rent_conditions = models.CharField(max_length=100, blank=True, null=True)
    prepayment = models.CharField(max_length=100, blank=True, null=True)
    parking = models.BooleanField(default=False)
    layout = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="rents")
    link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rent:rent_detail', args=[str(self.id)])


class RentImage(models.Model):
    apartment = models.ForeignKey(Rent, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="rent_images/")


class IDS(models.Model):
    rent_id = models.IntegerField(verbose_name='Монго id')
    status = models.CharField(verbose_name='Статус')