# Generated by Django 2.2.1 on 2019-05-15 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NationalityClean', '0009_auto_20190515_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filternationality',
            name='input_data',
        ),
        migrations.AddField(
            model_name='filternationality',
            name='verified_status',
            field=models.BooleanField(default=False),
        ),
    ]
