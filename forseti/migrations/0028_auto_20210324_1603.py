# Generated by Django 3.1.6 on 2021-03-24 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0027_auto_20210324_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='finaltable',
            name='fraction',
            field=models.CharField(blank=True, max_length=30, verbose_name='Фракция'),
        ),
        migrations.AddField(
            model_name='rowvote',
            name='populated',
            field=models.BooleanField(default=False, verbose_name='Заполнение FinalTable'),
        ),
    ]
