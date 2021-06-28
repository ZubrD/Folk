# Generated by Django 3.1.6 on 2021-04-29 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forseti', '0048_rules_status_quo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rules',
            name='status_quo',
            field=models.CharField(blank=True, choices=[('Рассмотрение', 'Рассмотрение'), ('Отклонение', 'Отклонение')], default='Рассмотрение', max_length=20, verbose_name='Статус'),
        ),
    ]
