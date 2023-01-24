from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Profile


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            _template_curr_index=1
        )

    def test_str_representation(self):
        self.assertEqual(str(self.profile), 'Profile of testuser')

    def test_current_set_template_index(self):
        self.assertEqual(self.profile.current_set_template_index, 1)

        self.profile._template_curr_index = None
        self.assertIsNone(self.profile.current_set_template_index)

    def test_set_template_curr_index(self):
        self.profile.set_template_curr_index(2)
        self.assertEqual(self.profile._template_curr_index, 2)

    def test__set_template_is_available(self):
        self.assertTrue(self.profile._set_template_is_available())

        self.profile._template_curr_index = None
        self.assertFalse(self.profile._set_template_is_available())

    def test__generate_default_set_name(self):
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.assertEqual(self.profile._generate_default_set_name(), 'ZZ-John_Doe')