from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


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




class QueueManager(models.Manager):
    def get_queryset(self):
        return super(QueueManager, self).get_queryset().filter(noti_que=True)

class Notification(models.Model):

    objects = models.Manager() #preserving old manager
    inqueue = QueueManager()

    TYPE_CHOICES = (
        ('RESPONSE', 'RESPONSE'),
        ('INFO', 'INFO'),
        ('OTHER', 'OTHER')
    )


    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True)
    noti_que = models.BooleanField(default=True)
    noti_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='INFO')
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')

    def __str__(self):
        return f'noti: {self.title}'

    class Meta:
        ordering=('-date_created',)



class Vote(models.Model):
    family = models.BooleanField(null=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"VOTE: {self.family}, {self.user}"

