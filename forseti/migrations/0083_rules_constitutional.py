# Generated by Django 3.1.6 on 2021-06-10 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0082_auto_20210609_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='constitutional',
            field=models.BooleanField(default=False, verbose_name='Поправка в Конституцию?'),
        ),
    ]
