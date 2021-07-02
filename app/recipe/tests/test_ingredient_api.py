from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class Public_ingredient_api_test(TestCase):
    """Test the publicly available ingredient api"""

    def setUp(self):
        self.client = APIClient()

    def test_longin_requiered(self):
        """Test that login is requierd to access the endpoint """
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class Private_ingredient_api_test(TestCase):
    """Testing privately avalable ingredient api user log in requiered"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='testing123',
        )
        0
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient(self):
        """Testing retrieving ingredients """
        Ingredient.objects.create(user=self.user, name='tomato')
        Ingredient.objects.create(user=self.user, name='potato')

        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_restricted_to_user(self):
        """Test that the returned is only for authorized user """
        user2 = get_user_model().objects.create_user(
            email='test12@gmail.com',
            password='password'
        )
        Ingredient.objects.create(user=user2, name='banana')
        ingredient = Ingredient.objects.create(user=self.user, name='chilli')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
