# Generated by Django 3.1.2 on 2020-10-29 03:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_ratings'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ratings',
            new_name='Rating',
        ),
    ]