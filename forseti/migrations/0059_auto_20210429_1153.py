# Generated by Django 3.1.6 on 2021-04-29 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0058_auto_20210429_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='branch',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Отрасль законодательства'),
        ),
    ]
