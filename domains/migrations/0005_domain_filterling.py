# Generated by Django 2.2.5 on 2020-08-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domains', '0004_auto_20200719_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='filterling',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]