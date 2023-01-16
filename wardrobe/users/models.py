from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from stuff.models import SetTemplate


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    _template_curr_index = models.IntegerField(blank=True, null=True)

    @property
    def current_set_template_index(self):
        return self._template_curr_index if self._set_template_is_available() else self._set_set_template_index()

    def __str__(self):
        return f'Profile of {self.user.username}'

    def _set_set_template_index(self):
        if SetTemplate.objects.all().exists():
            self._template_curr_index = SetTemplate.objects.first().id
        else:
            set_template = SetTemplate.objects.create(name='Default Set')
            set_template.save()
            self._template_curr_index = set_template.id
        return self._template_curr_index

    def set_template_curr_index(self, value):
        self._template_curr_index = value

    def _set_template_is_available(self):
        if self._template_curr_index:
            return SetTemplate.objects.filter(id=self._template_curr_index).exists()
        return self._set_set_template_index()
