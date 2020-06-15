from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

class PublishedManager(models.Manager): #Custom queryset manager
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


#creating the Post object; will have one to many relationship to User
class Post(models.Model):

    objects = models.Manager() #preserving old manager
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title
