# Generated by Django 3.1.6 on 2021-04-27 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0040_auto_20210402_1320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rules',
            name='author',
        ),
    ]
