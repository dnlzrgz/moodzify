from django.test import TestCase

from .models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword"))

    def test_string_representation(self):
        self.assertEqual(str(self.user), "test@example.com")

    def test_user_authentication(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertTrue(user.check_password("testpassword"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_superuser_creation(self):
        admin_user = CustomUser.objects.create_superuser(
            username="adminuser",
            email="admin@example.com",
            password="adminpassword",
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_permissions(self):
        user = CustomUser.objects.get(username="testuser")
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        user.is_staff = True
        user.save()

        self.assertTrue(user.is_staff)
