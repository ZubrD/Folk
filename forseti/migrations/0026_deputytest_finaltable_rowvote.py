# Generated by Django 3.1.6 on 2021-03-24 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0025_auto_20210322_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeputyTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя депутата')),
            ],
        ),
        migrations.CreateModel(
            name='FinalTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_number_final', models.CharField(max_length=20, verbose_name='Номер закона')),
                ('name', models.CharField(max_length=50, verbose_name='Имя депутата')),
                ('vote_result', models.CharField(max_length=10, verbose_name='Результат голосования')),
            ],
        ),
        migrations.CreateModel(
            name='RowVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_number_test', models.CharField(max_length=20, verbose_name='Номер закона')),
                ('yes_test', models.TextField(blank=True, max_length=10000, verbose_name='За')),
                ('no_test', models.TextField(blank=True, max_length=10000, verbose_name='Против')),
                ('abstained_test', models.TextField(blank=True, max_length=10000, verbose_name='Воздержались')),
                ('not_vote_test', models.TextField(blank=True, max_length=10000, verbose_name='Не голосовали')),
            ],
        ),
    ]
