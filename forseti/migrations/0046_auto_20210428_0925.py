# Generated by Django 3.1.6 on 2021-04-28 02:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0045_auto_20210428_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='initialization_date',
            field=models.DateField(default=datetime.date.today, verbose_name='На рассмотрении с'),
        ),
    ]