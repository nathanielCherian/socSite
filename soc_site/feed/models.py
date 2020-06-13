from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#creating the Post object; will have one to many relationship to User
class Post(models.Model): 
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

