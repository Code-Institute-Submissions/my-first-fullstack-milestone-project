# Generated by Django 3.1.2 on 2020-10-17 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20201017_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='country',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
