# Generated by Django 3.1.6 on 2021-04-29 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0050_auto_20210429_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='author',
            field=models.CharField(default='', max_length=400, verbose_name='Авторы'),
        ),
        migrations.AlterField(
            model_name='rules',
            name='branch',
            field=models.CharField(default='', max_length=100, verbose_name='Отрасль законодательства'),
        ),
    ]
