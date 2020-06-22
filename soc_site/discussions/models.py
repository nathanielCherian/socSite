from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Question(models.Model):
    
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=350)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        
        base_slug = slugify(self.title)
        
        i = ''
        while Question.objects.filter(slug=base_slug + str(i)):
            if i:
                i = str(int(i) + 1)
            else:
                i = '1'

        self.slug =  base_slug + i

        super(Question, self).save(*args, *kwargs)

class Response(models.Model):

    content = models.TextField()
    rating = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return self.content[:100]
