from django.utils.timezone import now
from django.test import TestCase
from .models import Category, ItemTemplate, Item, ItemRequired, SetTemplate, Set

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
        ItemTemplate.objects.create(
            name=ITEM_TYPE_NAME,
            description=ITEM_TYPE_DESCRIPTION,
            category=Category.objects.get(name=CATEGORY_NAME)
        )

    def test_item_type_is_valid(self):
        item_type = ItemTemplate.objects.get(name=ITEM_TYPE_NAME)
        self.assertEqual(item_type.name, ITEM_TYPE_NAME)
        self.assertEqual(item_type.description, ITEM_TYPE_DESCRIPTION)
        self.assertEqual(item_type.category.name, CATEGORY_NAME)


class ItemTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name=CATEGORY_NAME)
        ItemTemplate.objects.create(
            name=ITEM_TYPE_NAME,
            description=ITEM_TYPE_DESCRIPTION,
            category=Category.objects.get(name=CATEGORY_NAME)
        )
        Item.objects.create(
            type=ItemTemplate.objects.get(name=ITEM_TYPE_NAME)
        )

    def test_item_is_valid(self):
        item = Item.objects.get(id=1)
        self.assertEqual(item.type.name, ITEM_TYPE_NAME)
        self.assertEqual(item.status, ITEM_DEFAULT_STATUS)
        self.assertEqual(item.date_added.year, now().year)
        self.assertEqual(item.date_added.month, now().month)
        self.assertEqual(item.date_added.day, now().day)


class ItemRequiredTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name=CATEGORY_NAME)
        item_template = ItemTemplate.objects.create(
            name=ITEM_TYPE_NAME,
            description=ITEM_TYPE_DESCRIPTION,
            category=category,
        )
        ItemRequired.objects.create(item_type=item_template, quantity_required=2)

    def test_set_Template_is_valid(self):
        item_required = ItemRequired.objects.first()
        self.assertEqual(ITEM_TYPE_NAME, item_required.item_type.name)
