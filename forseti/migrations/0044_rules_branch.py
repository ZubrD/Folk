# Generated by Django 3.1.6 on 2021-04-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0043_auto_20210427_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='branch',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Отрасль'),
        ),
    ]
