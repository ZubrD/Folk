# Generated by Django 3.1.6 on 2021-06-02 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0077_auto_20210601_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='populi_voted',
            field=models.BooleanField(default=False, verbose_name='Народ проголосоал'),
        ),
    ]
