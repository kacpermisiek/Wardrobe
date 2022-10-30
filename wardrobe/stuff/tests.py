from django.utils.timezone import now
from django.test import TestCase
from .models import Category, ItemType, Item, ReservationEvent

CATEGORY_NAME = 'testing category'
ITEM_TYPE_NAME = 'item type name'
ITEM_TYPE_DESCRIPTION = 'some amazing description of item type object'
DEFAULT_ITEM_IMG_URL = '/media/default_item.png'
ITEM_DEFAULT_STATUS = 'Dostępny'


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name=CATEGORY_NAME)

    def test_category_is_valid(self):
        category = Category.objects.get(name=CATEGORY_NAME)
        self.assertEqual(category.name, CATEGORY_NAME)


class ItemTypeTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name=CATEGORY_NAME)
        ItemType.objects.create(
            name=ITEM_TYPE_NAME,
            description=ITEM_TYPE_DESCRIPTION,
            category=Category.objects.get(name=CATEGORY_NAME)
        )

    def test_item_type_is_valid(self):
        item_type = ItemType.objects.get(name=ITEM_TYPE_NAME)
        self.assertEqual(item_type.name, ITEM_TYPE_NAME)
        self.assertEqual(item_type.description, ITEM_TYPE_DESCRIPTION)
        self.assertEqual(item_type.category.name, CATEGORY_NAME)
        self.assertEqual(item_type.image.url, DEFAULT_ITEM_IMG_URL)


class ItemTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name=CATEGORY_NAME)
        ItemType.objects.create(
            name=ITEM_TYPE_NAME,
            description=ITEM_TYPE_DESCRIPTION,
            category=Category.objects.get(name=CATEGORY_NAME)
        )
        Item.objects.create(
            type=ItemType.objects.get(name=ITEM_TYPE_NAME)
        )

    def test_item_is_valid(self):
        item = Item.objects.get(id=1)
        self.assertEqual(item.type.name, ITEM_TYPE_NAME)
        self.assertEqual(item.status, ITEM_DEFAULT_STATUS)
        self.assertEqual(item.date_added.year, now().year)
        self.assertEqual(item.date_added.month, now().month)
        self.assertEqual(item.date_added.day, now().day)
