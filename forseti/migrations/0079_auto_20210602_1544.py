# Generated by Django 3.1.6 on 2021-06-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0078_rules_populi_voted'),
    ]

    operations = [
        migrations.AddField(
            model_name='rules',
            name='result_deputy_vote',
            field=models.CharField(default='', max_length=10, verbose_name='Результат голосования депутатов'),
        ),
        migrations.AddField(
            model_name='rules',
            name='result_populi_vote',
            field=models.CharField(default='', max_length=10, verbose_name='Результат голосования народа'),
        ),
        migrations.AlterField(
            model_name='rules',
            name='populi_voted',
            field=models.BooleanField(default=False, verbose_name='Народ проголосовал'),
        ),
    ]