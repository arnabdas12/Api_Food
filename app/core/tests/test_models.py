from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test to create user with email is successful """
        email = 'Test@whats.com'
        password = 'testing123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password

        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that the new user email is normalized """
        email = "test@WHATS.COM"
        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_creting_user_with_no_email_check(self):
        """Test if no emailID passed wile creating a new user"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test1234")

    def test_create_new_super_user(self):
        """Test if super user is created """
        user = get_user_model().objects.create_superuser(
            email='Test@whats.com',
            password='testing123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
