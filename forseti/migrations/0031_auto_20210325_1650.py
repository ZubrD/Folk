# Generated by Django 3.1.6 on 2021-03-25 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0030_rules_populated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deputy',
            name='party_fraction',
            field=models.CharField(default='', max_length=50, verbose_name='Фракция'),
        ),
    ]
