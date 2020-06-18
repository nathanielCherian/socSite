from django.db import models
from django.conf import settings
from django.urls import reverse
from django.template.defaultfilters import slugify


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/')
    social_link = models.CharField(max_length=300, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)
    establishment = models.CharField(max_length=300, blank=True, null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'profile for {self.user.username}'

    class Meta:
        unique_together = ('user', 'slug')



