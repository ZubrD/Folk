# Generated by Django 3.1.6 on 2021-04-27 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0042_auto_20210427_1129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rules',
            name='author_2',
        ),
        migrations.AddField(
            model_name='rules',
            name='author',
            field=models.CharField(blank=True, default='', max_length=400, verbose_name='Авторы'),
        ),
    ]
