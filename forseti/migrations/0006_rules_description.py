# Generated by Django 3.1.6 on 2021-02-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0005_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='description',
            field=models.CharField(default='', max_length=10000, verbose_name='Описание'),
        ),
    ]
