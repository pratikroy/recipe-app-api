from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from unittest.mock import patch


def sample_user(email='demouser@mymail.com', password='password'):
    """create a sample user"""
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
                    user=sample_user(),
                    name='Sample name'
                )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
                    user=sample_user(),
                    name='Cucumber'
                )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
                    user=sample_user(),
                    title='Steak and mushroom sauce',
                    time_minutes=5,
                    price=5.00
                )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is stored in correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
