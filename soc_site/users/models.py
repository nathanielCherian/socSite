from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'slug')

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})