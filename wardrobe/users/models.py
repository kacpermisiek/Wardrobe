from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from stuff.models import CurrentSetTemplate


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    curr_set_template = models.OneToOneField(CurrentSetTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        try:
            self.curr_set_template
        except AttributeError:
            self.curr_set_template = CurrentSetTemplate.objects.create()

        super().save()

        image = Image.open(self.image.path).convert('RGB')
        
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.convert('RGB').save(self.image.path)

        image.close()  # TODO Not sure if it's necessary
