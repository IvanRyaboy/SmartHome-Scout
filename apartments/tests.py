from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from apartments.models import Apartment, Building, Location, Town, Region, ApartmentImage


class ApartmentsViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = Region.objects.create(name="Test Region")
        cls.town = Town.objects.create(name="Test Town", region=cls.region)
        cls.location = Location.objects.create(
            town=cls.town,
            district="Test District",
            microdistrict="Test Microdistrict",
            street="Test Street",
            house_number="10",
            latitude=55.0,
            longitude=37.0
        )
        cls.building = Building.objects.create(
            location=cls.location,
            floors_total=10,
            wall_material="Brick",
            construction_year=2000,
            house_amenities="Elevator",
            parking="Garage"
        )
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        cls.apartment = Apartment.objects.create(
            title="Test Apartment",
            price=100000,
            building=cls.building,
            total_area=70,
            living_area=50,
            kitchen_area=10,
            balcony=True,
            balcony_type=Apartment.Balcony.CLASSIC,
            balcony_area=5.5,
            room_count=3,
            description="Nice apartment",
            owner=cls.user,
            floor=3,
            sale_conditions=Apartment.Sale.OPEN,
            bathroom_count=2,
            ceiling_height=2.8,
            renovation="Good",
            condition=Apartment.Condition.GOOD,
            contract_number="123ABC",
            contract_date=None,
            level_count=1,
            ownership_type=Apartment.Ownership.PRIVATE
        )

    def setUp(self):
        # Клиент без авторизации
        self.client = Client()

    def test_apartments_home_view_status_and_template(self):
        url = reverse('apartments:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apartments/apartments_list.html")
        self.assertIn(self.apartment, response.context['object_list'] or [])

    def test_apartments_home_filter_price(self):
        url = reverse('apartments:home') + f'?price__gte={self.apartment.price + 1}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.apartment, response.context['object_list'] or [])

    def test_apartment_detail_view(self):
        url = reverse('apartments:apartment_detail', kwargs={'pk': self.apartment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "apartments/apartment_view.html")
        self.assertEqual(response.context['apartment'], self.apartment)

    def test_add_apartment_view_requires_login(self):
        url = reverse('apartments:add_apartment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Редирект на логин

    def test_add_apartment_view_get(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('apartments:add_apartment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apartments/add_apartment.html')
        self.assertIn('form', response.context)

    def test_add_apartment_view_post_valid(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('apartments:add_apartment')

        data = {
            'region': self.region.id,
            'town_name': self.town.name,
            'district': 'District',
            'microdistrict': '',
            'street': 'Test Street 2',
            'house_number': '5',
            'floors_total': 5,
            'wall_material': 'Brick',
            'construction_year': 1990,
            'house_amenities': 'Elevator',
            'parking': 'Yes',
            # Обязательные для модели Apartment:
            'price': 123456,
            'total_area': 60,
            'living_area': 40,
            'kitchen_area': 10,
            'balcony': True,
            'balcony_type': Apartment.Balcony.CLASSIC,
            'balcony_area': 3.5,
            'room_count': 2,
            'description': 'Test description',
            'floor': 2,
            'sale_conditions': Apartment.Sale.OPEN,
            'bathroom_count': 1,
            'ceiling_height': 2.5,
            'renovation': 'Good',
            'condition': Apartment.Condition.GOOD,
            'contract_number': 'ABC123',
            'level_count': 1,
            'ownership_type': Apartment.Ownership.PRIVATE,
            'title': 'Test Apartment'
        }

        img = SimpleUploadedFile(
            'test_image.jpg',
            b'file_content_here',
            content_type='image/jpeg'
        )

        response = self.client.post(url, data=data, files=[('image', img)])
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Apartment.objects.filter(owner=self.user).exists())
        apartment = Apartment.objects.filter(owner=self.user).order_by('-id').first()
        self.assertEqual(apartment.title, 'Test Apartment')

    def test_update_apartment_view_owner_access(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('apartments:update_apartment', kwargs={'pk': self.apartment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apartments/add_apartment.html')

    def test_update_apartment_view_other_user_forbidden(self):
        other_user = get_user_model().objects.create_user(username='other', password='pass123')
        self.client.login(username='other', password='pass123')
        url = reverse('apartments:update_apartment', kwargs={'pk': self.apartment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access denied", status_code=403)

    def test_delete_apartment_view_owner_access(self):
        self.client.login(username='testuser', password='password123')
        url = reverse('apartments:delete_apartment', kwargs={'pk': self.apartment.pk})
        response = self.client.post(url)
        # Проверяем, что после удаления редирект на список квартир
        self.assertRedirects(response, reverse('apartments:home'))
        self.assertFalse(Apartment.objects.filter(pk=self.apartment.pk).exists())

    def test_delete_apartment_view_other_user_forbidden(self):
        other_user = get_user_model().objects.create_user(username='other', password='pass123')
        self.client.login(username='other', password='pass123')
        url = reverse('apartments:delete_apartment', kwargs={'pk': self.apartment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertContains(response, "Access denied", status_code=403)
