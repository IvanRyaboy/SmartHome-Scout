from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
import uuid


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


class SignUpPageTest(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class ProfilePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        cls.user_2 = get_user_model().objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password456'
        )
        cls.url_user_1 = reverse('accounts:profile', kwargs={'pk': cls.user_1.pk})

    def test_access_profile_with_login_and_owner(self):
        self.client.login(username='user1', password='password123')
        response = self.client.get(self.url_user_1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user_1.username)

    def test_access_profile_denied_for_other_user(self):
        self.client.login(username='user2', password='password456')
        response = self.client.get(self.url_user_1)
        self.assertContains(response, "Access denied", status_code=403)

    def test_access_profile_redirect_for_anonymous(self):
        response = self.client.get(self.url_user_1)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn(response.status_code, (302, 301))
