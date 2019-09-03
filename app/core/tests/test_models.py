from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email(self):
        """Test creating new user using email and check for success"""
        email = "test@mymail.com"
        password = "password@789"
        user = get_user_model().objects.create_user(
                email=email,
                password=password
                )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        """Test the email for new user is normalized"""
        email = "test@MYMAIL.COM"
        password = "password@123"
        user = get_user_model().objects.create_user(
                email=email, password=password)

        self.assertEqual(user.email, email.lower())

    def test_email_is_invalid(self):
        """Test the newly created email address is valid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'password@123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
                "super@mymail.com",
                "password@789")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)