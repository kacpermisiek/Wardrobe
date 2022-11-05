from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

# TODO Align UTs
# class ProfileCreationTestCase(TestCase):
#     def setUp(self):
#         user = User.objects.create(
#             username='username',
#             first_name='user',
#             last_name='name',
#             email='asd@uwr.edu.pl',
#             password='testing321'
#         )
#         Profile.objects.create(user=User.objects.first())
#
#     def test_profile_is_valid(self):
#         profile = Profile.objects.get(user__username='username')
#         self.assertEqual('default.png', profile.image.url)
