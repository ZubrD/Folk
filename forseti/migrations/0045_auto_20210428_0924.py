# Generated by Django 3.1.6 on 2021-04-28 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0044_rules_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='branch',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Отрасль законодательства'),
        ),
    ]
