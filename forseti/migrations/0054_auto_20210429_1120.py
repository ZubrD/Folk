# Generated by Django 3.1.6 on 2021-04-29 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0053_auto_20210429_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='voting_date',
            field=models.DateField(blank=True, default=None, verbose_name='Дата голосования'),
        ),
    ]
