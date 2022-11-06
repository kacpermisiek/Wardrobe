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
        return self._template_curr_index if self._template_curr_index else self._set_template_index()

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.image.path).convert('RGB')
        
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.convert('RGB').save(self.image.path)

        image.close()  # TODO Not sure if it's necessary

    def _set_template_index(self):
        if SetTemplate.objects.all().exists():
            self._template_curr_index = SetTemplate.objects.first().id
        else:
            set_template = SetTemplate.objects.create(name='Default Set')
            set_template.save()
            self._template_curr_index = set_template.id
        return self._template_curr_index

