# Generated by Django 3.0.7 on 2020-06-27 23:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200618_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('noti_que', models.BooleanField(default=True)),
                ('noti_type', models.CharField(choices=[('INFO', 'INFO'), ('OTHER', 'OTHER')], default='INFO', max_length=10)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='users.Profile')),
            ],
            options={
                'ordering': ('-date_created',),
            },
        ),
    ]
