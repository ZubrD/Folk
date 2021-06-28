# Generated by Django 3.1.6 on 2021-03-26 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0034_auto_20210326_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deputy',
            name='party_fraction',
            field=models.CharField(choices=[('Единая Россия', 'Единая Россия'), ('КПРФ', 'КПРФ'), ('Справедливая Россия', 'Справедливая Россия'), ('ЛДПР', 'ЛДПР'), ('Вне фракций', 'Вне фракций')], max_length=50, verbose_name='Фракция'),
        ),
    ]