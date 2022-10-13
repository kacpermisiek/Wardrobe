from django.test import TestCase
from .models import Category


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name='testing_category')

    def test_category_is_valid(self):
        category = Category.objects.get(name='testing_category')
        self.assertEqual(category.name, 'testing_category')
