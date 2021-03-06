from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from taggit.managers import TaggableManager
from markdownx.models import MarkdownxField
from bs4 import BeautifulSoup
from random import randint



class PublishedManager(models.Manager): #Custom queryset manager
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published', active=True)


#creating the Post object; will have one to many relationship to User
class Post(models.Model):

    objects = models.Manager() #preserving old manager
    published = PublishedManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=100, unique=False)
    slug = models.SlugField(max_length=100)
    summary = models.CharField(max_length=300)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs): #system of producing unique slugs :)

        slugged_title = slugify(self.title, allow_unicode=True)

        if not slugged_title:
            slugged_title = 'dont-use-emojis'

        post_family = Post.objects.filter(author=self.author)

        similar_posts = post_family.filter(slug=slugged_title)

        i = 10
        while len(similar_posts) > 1:
            slugged_title += str(randint(0, i))
            similar_posts = post_family.filter(slug=slugged_title)
            i *= i

        """
        slug_posts = Post.objects.filter(slug=slugged_title)
        if slug_posts:
            slugged_title += str(len(slug_posts))
        """

        self.slug =  slugged_title

        #self.content = purge_html(self.content) #cleans HTML to prevent injection attack


        super(Post, self).save(*args, *kwargs)



def purge_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    evil = ['script', 'form', 'button','article','aside','body','details','head','html',
        'footer','nav','section','summary','base','basefont','link','meta','style',
        'title','button','datalist','fieldset','form','input','keygen','label','legend',
        'meter','optgroup','option','select','textarea','script','noscript','applet',
        'object',
        ]

    for element in evil:
        for s in soup.find_all(element):
            print(s)
            s.decompose()

    return str(soup)