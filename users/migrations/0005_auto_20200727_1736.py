# Generated by Django 2.2.5 on 2020-07-27 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200719_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=300),
        ),
    ]
