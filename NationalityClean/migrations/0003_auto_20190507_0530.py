# Generated by Django 2.2.1 on 2019-05-07 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NationalityClean', '0002_auto_20190507_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekeruserdetail',
            name='score',
            field=models.FloatField(null=True),
        ),
    ]