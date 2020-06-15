# Generated by Django 3.0.7 on 2020-06-15 04:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='users/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='social_link',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('user', 'slug')},
        ),
    ]