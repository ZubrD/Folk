# Generated by Django 3.1.6 on 2021-02-02 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PartyFraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=30)),
            ],
            options={
                'verbose_name': 'Фракция',
                'verbose_name_plural': 'Фракции',
            },
        ),
    ]