# Generated by Django 3.1.6 on 2021-05-19 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0068_auto_20210519_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='deputy',
            name='short_name',
            field=models.CharField(default='', max_length=150, verbose_name='ФИО с инициалами'),
        ),
    ]
