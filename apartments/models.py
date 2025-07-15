import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Region(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название области')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Область'
        verbose_name_plural = 'Области'


class Town(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название города')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='towns', verbose_name='Область')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Location(models.Model):
    town = models.ForeignKey(Town,
                             on_delete=models.CASCADE,
                             related_name='locations',
                             verbose_name='Населённый пункт')
    district = models.CharField(max_length=255, verbose_name='Район', blank=True)
    microdistrict = models.CharField(max_length=255, verbose_name='Микрорайон', blank=True)
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=255, verbose_name='Номер дома')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')

    def __str__(self):
        return f"{self.town.name}, ул. {self.street}, д. {self.house_number}"

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'


class Building(models.Model):
    location = models.OneToOneField(Location,
                                    on_delete=models.CASCADE,
                                    related_name='house',
                                    verbose_name='Местоположение')
    floors_total = models.IntegerField(verbose_name='Этажность')
    wall_material = models.CharField(max_length=100, verbose_name='Материал стен', blank=True)
    construction_year = models.PositiveIntegerField(verbose_name='Год постройки', blank=True, null=True)
    house_amenities = models.CharField(verbose_name='Обустройство дома', blank=True, max_length=255)
    parking = models.CharField(max_length=255, verbose_name='Парковка', blank=True)

    def __str__(self):
        return f"Дом на {self.location}"

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'


class Apartment(models.Model):
    class Balcony(models.TextChoices):
        CLASSIC = 'Classic', 'Классический'
        FRENCH = 'French', 'Французский'
        EXTENDED = 'Extended', 'С выносом'
        LOGGIA = 'Loggia', 'Лоджия'

    class Sale(models.TextChoices):
        ALTERNATIVE = 'Alternative', 'Альтернативная продажа'
        OPEN = 'Open', 'Свободная продажа'
        CONDITION = 'Condition', 'С условиями'

    class Condition(models.TextChoices):
        NEW = 'New', 'Новое'
        ALMOST = 'Almost', 'Почти новое'
        GOOD = 'Good', 'Хорошее'
        FAIR = 'Fair', 'Удовлетворительное'
        RENOVATION = 'Renovation', 'Требующее ремонта'
        UNINHABITABLE = 'Uninhabitable', 'Аварийное'

    class Ownership(models.TextChoices):
        STATE = 'State', 'Государственная'
        PRIVATE = 'Private', 'Частная'
        SHARED = 'Shared', 'Общая долевая'
        JOINT = 'Joint', 'Общая совместная'
        COLLECTIVE = 'Collective', 'Коллективная'
        FOREIGN = 'Foreign', 'Иностранная'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    title = models.CharField(verbose_name='Название', default='Купить квартиру')
    price = models.FloatField(verbose_name='Цена')
    building = models.ForeignKey(Building,
                                 on_delete=models.CASCADE,
                                 related_name='apartments',
                                 verbose_name='Дом')
    total_area = models.FloatField(verbose_name='Общая площадь')
    living_area = models.FloatField(verbose_name='Жилая площадь')
    kitchen_area = models.FloatField(verbose_name='Площадь кухни', blank=True, null=True)
    balcony_area = models.FloatField(verbose_name='Площадь балкона', blank=True, null=True)
    balcony = models.BooleanField(verbose_name='Балкон')
    balcony_type = models.CharField(choices=Balcony.choices,
                                    verbose_name='Тип балкона',
                                    blank=True,
                                    null=True,
                                    default=None)
    room_count = models.IntegerField(verbose_name='Количество комнат')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name="apartments",
                              verbose_name='Владелец')
    floor = models.IntegerField(verbose_name='Этаж')
    sale_conditions = models.CharField(choices=Sale.choices,
                                       verbose_name='Условия продажи',
                                       default=Sale.OPEN,
                                       max_length=20)
    bathroom_count = models.IntegerField(verbose_name='Количество санузлов', blank=True, null=True)
    ceiling_height = models.FloatField(verbose_name='Высота потолков', blank=True, null=True)
    renovation = models.CharField(max_length=100, verbose_name='Ремонт', blank=True)
    condition = models.CharField(choices=Condition.choices,
                                 verbose_name='Состояние',
                                 blank=True,
                                 default=Condition.NEW,
                                 max_length=20)
    contract_number = models.CharField(verbose_name='Номер договора', blank=True, max_length=255)
    contract_date = models.DateTimeField(verbose_name='Дата договора', blank=True, null=True)
    level_count = models.IntegerField(verbose_name='Число уровней', blank=True, null=True)
    ownership_type = models.CharField(choices=Ownership.choices,
                                      verbose_name='Собственность',
                                      blank=True,
                                      default=Ownership.PRIVATE,
                                      max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('apartments:flat_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
