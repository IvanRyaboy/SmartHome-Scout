import django_filters
from django import forms
from django_filters.widgets import BooleanWidget

from .models import Apartment


class ApartmentFilter(django_filters.FilterSet):
    price__gte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        label='Price from (₽)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 0
        })
    )

    price__lte = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        label='Price to (₽)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'To',
            'min': 0
        })
    )

    room_count__gte = django_filters.NumberFilter(
        field_name='room_count',
        lookup_expr='gte',
        label='Rooms (min)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min',
            'min': 1
        })
    )

    room_count__exact = django_filters.NumberFilter(
        field_name='room_count',
        lookup_expr='exact',
        label='Exact number of rooms',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Exact value',
            'min': 1
        })
    )

    floor__gte = django_filters.NumberFilter(
        field_name='floor',
        lookup_expr='gte',
        label='Floor from',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 1
        })
    )

    floor__exact = django_filters.NumberFilter(
        field_name='floor',
        lookup_expr='exact',
        label='Exact floor',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Exact floor',
            'min': 1
        })
    )

    total_area__gte = django_filters.NumberFilter(
        field_name='total_area',
        lookup_expr='gte',
        label='Total area from (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 0,
            'step': '0.1'
        })
    )

    total_area__lte = django_filters.NumberFilter(
        field_name='total_area',
        lookup_expr='lte',
        label='Total area to (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'To',
            'min': 0,
            'step': '0.1'
        })
    )

    living_area__gte = django_filters.NumberFilter(
        field_name='living_area',
        lookup_expr='gte',
        label='Living area from (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 0,
            'step': '0.1'
        })
    )

    living_area__lte = django_filters.NumberFilter(
        field_name='living_area',
        lookup_expr='lte',
        label='Living area to (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'To',
            'min': 0,
            'step': '0.1'
        })
    )

    kitchen_area__gte = django_filters.NumberFilter(
        field_name='kitchen_area',
        lookup_expr='gte',
        label='Kitchen area from (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 0,
            'step': '0.1'
        })
    )

    kitchen_area__lte = django_filters.NumberFilter(
        field_name='kitchen_area',
        lookup_expr='lte',
        label='Kitchen area to (m²)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'To',
            'min': 0,
            'step': '0.1'
        })
    )

    ceiling_height__gte = django_filters.NumberFilter(
        field_name='ceiling_height',
        lookup_expr='gte',
        label='Ceiling height from (m)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'From',
            'min': 0,
            'step': '0.1'
        })
    )

    ceiling_height__exact = django_filters.NumberFilter(
        field_name='ceiling_height',
        lookup_expr='exact',
        label='Exact ceiling height (m)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Exact value',
            'min': 0,
            'step': '0.1'
        })
    )

    balcony = django_filters.BooleanFilter(
        field_name='balcony',
        label='Balcony',
        widget=BooleanWidget(),
    )

    class Meta:
        model = Apartment
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters = {
            'price__gte': self.filters['price__gte'],
            'price__lte': self.filters['price__lte'],
            'room_count__exact': self.filters['room_count__exact'],
            'room_count__gte': self.filters['room_count__gte'],
            'floor__exact': self.filters['floor__exact'],
            'floor__gte': self.filters['floor__gte'],
            'total_area__gte': self.filters['total_area__gte'],
            'total_area__lte': self.filters['total_area__lte'],
            'living_area__gte': self.filters['living_area__gte'],
            'living_area__lte': self.filters['living_area__lte'],
            'kitchen_area__gte': self.filters['kitchen_area__gte'],
            'kitchen_area__lte': self.filters['kitchen_area__lte'],
            'ceiling_height__exact': self.filters['ceiling_height__exact'],
            'ceiling_height__gte': self.filters['ceiling_height__gte'],
            'balcony': self.filters['balcony'],
        }
