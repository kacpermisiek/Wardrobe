from datetime import date

from django.contrib.auth.models import User, Group
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.utils.timezone import now
from django.test import TestCase
from .models import Category, ItemTemplate, Item, ItemRequired, SetTemplate, Set
from .views import ItemTemplateDeleteView

CATEGORY_NAME = 'testing category'
ITEM_TEMPLATE_NAME = 'item type name'
ITEM_TYPE_DESCRIPTION = 'some amazing description of item type object'
SET_TEMPLATE_NAME = "Default Set Template Name"
DEFAULT_ITEM_IMG_URL = '/media/default_item.png'
ITEM_DEFAULT_STATUS = 'Dostępny'


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item1 = Item.objects.create(type=ItemTemplate.objects.create(name="Test Item 1", category=self.category))
        self.item2 = Item.objects.create(type=ItemTemplate.objects.create(name="Test Item 2", category=self.category))

    def test_num_of_objects(self):
        self.assertEqual(self.category.num_of_objects, 2)


class ItemTemplateTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item_template = ItemTemplate.objects.create(name="Test Item Template", category=self.category)
        self.item1 = Item.objects.create(type=self.item_template, status='Dostępny')
        self.item2 = Item.objects.create(type=self.item_template, status='Uszkodzony')

    def test_quantity(self):
        self.assertEqual(self.item_template.quantity, 2)


class ItemRequiredTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item_template = ItemTemplate.objects.create(name="Test Item Template", category=self.category)
        self.item_required = ItemRequired.objects.create(quantity_required=2, item_type=self.item_template)

    def test_required_quantity(self):
        self.assertEqual(self.item_required.quantity_required, 2)

    def test_str(self):
        self.assertEqual(self.item_required.__str__(), "item type: Test Item Template")


class SetTemplateTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item_template1 = ItemTemplate.objects.create(name="Test Item Template 1", category=self.category)
        self.item_template2 = ItemTemplate.objects.create(name="Test Item Template 2", category=self.category)
        self.item_required1 = ItemRequired.objects.create(quantity_required=3, item_type=self.item_template1)
        self.item_required2 = ItemRequired.objects.create(quantity_required=2, item_type=self.item_template2)
        self.user = User.objects.create()
        self.set_template = SetTemplate.objects.create(name=SET_TEMPLATE_NAME, created_by=self.user)

        self.set_template.items_required.add(self.item_required1)
        self.set_template.items_required.add(self.item_required2)

    def test_str(self):
        self.assertEqual(f'SetTemplate object name: {SET_TEMPLATE_NAME}', self.set_template.__str__())

    def test_items_required(self):
        self.assertEqual(self.set_template.items_required.count(), 2)
        self.assertEqual(self.set_template.items_required.first().item_type.name, "Test Item Template 1")
        self.assertEqual(self.set_template.items_required.last().item_type.name, "Test Item Template 2")

    def test_created_by(self):
        self.set_template.created_by = self.user
        self.set_template.save()
        self.assertEqual(self.set_template.created_by, self.user)


class SetTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item_template1 = ItemTemplate.objects.create(name="Test Item Template 1", category=self.category)
        self.item_template2 = ItemTemplate.objects.create(name="Test Item Template 2", category=self.category)
        self.item_required1 = ItemRequired.objects.create(quantity_required=3, item_type=self.item_template1)
        self.item_required2 = ItemRequired.objects.create(quantity_required=2, item_type=self.item_template2)
        self.user = User.objects.create()
        self.set_template = SetTemplate.objects.create(name=SET_TEMPLATE_NAME, ready=True, created_by=self.user)
        self.set_template.items_required.add(self.item_required1)
        self.set_template.items_required.add(self.item_required2)

        self.set = Set.objects.create(set_template=self.set_template)
        self.item1 = Item.objects.create(type=self.item_template1, item_set=self.set)
        self.item2 = Item.objects.create(type=self.item_template2, item_set=self.set)

    def test_str(self):
        self.assertEqual(self.set.__str__(), "Set object")

    def test_set_template(self):
        self.assertEqual(self.set.set_template, self.set_template)

    def test_items(self):
        self.assertEqual(self.set.items.count(), 2)
        self.assertEqual(self.set.items.first(), self.item1)

    def test_set_status(self):
        self.set.set_status = 'Dostępny'
        self.set.save()
        self.assertEqual(self.set.set_status, 'Dostępny')


class ItemTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name=CATEGORY_NAME)
        self.item_template = ItemTemplate.objects.create(name=ITEM_TEMPLATE_NAME, category=self.category)
        self.item = Item.objects.create(type=self.item_template)
        self.user = User.objects.create()

    def test_str(self):
        self.assertEqual(self.item.__str__(), f"({self.item.id}) {ITEM_TEMPLATE_NAME}")

    def test_type(self):
        self.assertEqual(self.item.type, self.item_template)

    def test_status(self):
        self.item.status = 'Dostępny'
        self.item.save()
        self.assertEqual(self.item.status, 'Dostępny')

    def test_item_set(self):
        set_template = SetTemplate.objects.create(name=SET_TEMPLATE_NAME, created_by=self.user)
        item_set = Set.objects.create(set_template=set_template)
        self.item.item_set = item_set
        self.item.save()
        self.assertEqual(self.item.item_set, item_set)

    def test_date_added(self):
        self.assertEqual(self.item.date_added.date(), date.today())

    def test_badge_status(self):
        self.assertEqual(self.item.badge_status, 'success')


class HomeViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username='superuser', password='password',
                                                  is_superuser=True, is_staff=True)
        self.staff_user = User.objects.create_user(username='staffuser', password='password',
                                                   is_staff=True, is_superuser=False)
        self.normal_user = User.objects.create_user(username='normaluser', password='password',
                                                    is_staff=False, is_superuser=False)
        self.set_by_superuser = SetTemplate.objects.create(name='Set by superuser',
                                                           created_by=self.superuser, ready=False)
        self.set_by_superuser_ready = SetTemplate.objects.create(name='Set2 by superuser that is ready',
                                                           created_by=self.superuser, ready=True)
        self.set_by_staff_user = SetTemplate.objects.create(name='Set by staff user',
                                                            created_by=self.staff_user, ready=False)

    def test_home_view_superuser(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('stuff-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/home.html')
        self.assertContains(response, 'Set by superuser')
        self.assertContains(response, 'Set2 by superuser that is ready')
        self.assertContains(response, 'Set by staff user')
        self.assertContains(response, 'Aktualny zestaw')

    def test_home_view_normal_user(self):
        self.client.login(username='normaluser', password='password')
        response = self.client.get(reverse('stuff-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/home.html')
        self.assertContains(response, 'Set2 by superuser that is ready')
        self.assertNotContains(response, 'Set by superuser')
        self.assertNotContains(response, 'Set by staff user')
        self.assertNotContains(response, 'Aktualny zestaw')

    def test_home_view_staff_user(self):
        self.client.login(username='staffuser', password='password')
        response = self.client.get(reverse('stuff-home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/home.html')

        self.assertContains(response, 'Set2 by superuser that is ready')
        self.assertContains(response, 'Set by staff user')
        self.assertContains(response, 'Aktualny zestaw')

        self.assertNotContains(response, 'Set by superuser')

    def test_home_view_anonymous(self):
        response = self.client.get(reverse('stuff-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/home.html')

        self.assertContains(response, "Zaloguj się, aby")

        self.assertNotContains(response, 'Set2 by superuser that is ready')
        self.assertNotContains(response, 'Set by superuser')
        self.assertNotContains(response, 'Set by staff user')
        self.assertNotContains(response, 'Aktualny zestaw')


class CategoryListViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')
        self.category3 = Category.objects.create(name='category3')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/category/list.html')

    def test_view_context_data(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), [self.category1, self.category2, self.category3])

    def test_view_ordering(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['categories']), [self.category1, self.category2, self.category3])


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.category2 = Category.objects.create(name='category2')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/category/form.html')

    def test_view_context_data(self):
        response = self.client.get(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['category'], self.category1)

    def test_view_404_status(self):
        response = self.client.get(reverse('category-detail', args=[0]))
        self.assertEqual(response.status_code, 404)


class CategoryCreateViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.normal_user = User.objects.create_user(username='normaluser', password='password')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get('/category/new')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-create'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/category/create.html')

    def test_view_redirects_normal_user(self):
        self.client.login(username='normaluser', password='password')
        response = self.client.get(reverse('category-create'))
        self.assertEqual(response.status_code, 403)

    def test_view_creating_category_superuser(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('category-create'), {'name': 'Test Category'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.filter(name='Test Category').count(), 1)


class CategoryUpdateViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.normal_user = User.objects.create_user(username='normaluser', password='password')
        self.category = Category.objects.create(name='Test category')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(f'/category/{self.category.id}/update')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-update', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-update', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, 200)


class CategoryDeleteViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.normal_user = User.objects.create_user(username='normaluser', password='password')
        self.category = Category.objects.create(name='Test category')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(f'/category/{self.category.id}/delete')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-delete', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('category-delete', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_deletes_category(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('category-delete', kwargs={'pk': self.category.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 0)


class ItemTemplateCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True, is_superuser=True)
        self.category = Category.objects.create(name='Test Category')
        self.data = {
            'name': 'Test Item',
            'category': self.category.id
        }

    def test_create_item_template(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('item-template-create'), data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ItemTemplate.objects.count(), 1)
        self.assertEqual(ItemTemplate.objects.first().name, 'Test Item')

        self.assertRedirects(response, reverse('item-template-list'))

class ItemTemplateDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password', is_staff=True, is_superuser=True)
        self.category = Category.objects.create(name='Test Category')
        self.item_template = ItemTemplate.objects.create(name='Item Template name', category=self.category)

    def test_detail_view_url_exists(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item-template-detail', args=[self.item_template.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_url_accessible_by_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item-template-detail', args=[self.item_template.id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item-template-detail', args=[self.item_template.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/item_template/detail.html')

    def test_detail_view_shows_item_name(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item-template-detail', args=[self.item_template.id]))
        self.assertContains(response, 'Item Template name')

    def test_detail_view_shows_item_category(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('item-template-detail', args=[self.item_template.id]))
        self.assertContains(response, 'Test Category')


class ItemTemplateUpdateViewTest(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.normal_user = User.objects.create_user(username='normaluser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.item_template = ItemTemplate.objects.create(name='Test Item', category=self.category)
        self.data = {
            'name': 'Updated Item',
            'category': self.category.id
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('item-template-update', kwargs={'pk': self.item_template.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('item-template-update', kwargs={'pk': self.item_template.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='superuser', password='password')
        response = self.client.get(reverse('item-template-update', kwargs={'pk': self.item_template.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stuff/item_template/form.html')

    def test_view_redirects_normal_user(self):
        self.client.login(username='normaluser', password='password')
        response = self.client.get(reverse('item-template-update', kwargs={'pk': self.item_template.id}))
        self.assertEqual(response.status_code, 403)

    def test_view_updates_item_template(self):
        self.client.login(username='superuser', password='password')
        response = self.client.post(reverse('item-template-update', kwargs={'pk': self.item_template.id}), data=self.data)

        self.item_template.refresh_from_db()
        self.assertEqual(self.item_template.name, 'Updated Item')
        self.assertRedirects(response, reverse('item-template-detail', kwargs={'pk': self.item_template.id}))


