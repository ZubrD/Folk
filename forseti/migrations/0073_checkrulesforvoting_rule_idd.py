# Generated by Django 3.1.6 on 2021-05-27 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0072_auto_20210527_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkrulesforvoting',
            name='rule_idd',
            field=models.CharField(default='', max_length=10, verbose_name='ID закона'),
        ),
    ]