# Generated by Django 3.1.6 on 2021-03-30 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0038_auto_20210329_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoxPopuli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='Кто проголосовал')),
                ('rule_number', models.CharField(default='', max_length=20, verbose_name='Номер закона')),
                ('result', models.CharField(max_length=15, verbose_name='Как проголосовал')),
            ],
        ),
    ]
