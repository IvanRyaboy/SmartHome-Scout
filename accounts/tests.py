from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='John', email='john@mail.ru', password='testpass123'
        )
        self.assertEqual(user.username, 'John')
        self.assertEqual(user.email, 'john@mail.ru')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='SuperJohn', email='superjohn@mail.ru', password='testpass123'
        )
        self.assertEqual(admin_user.username, 'SuperJohn')
        self.assertEqual(admin_user.email, 'superjohn@mail.ru')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
