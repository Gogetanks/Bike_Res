# Generated by Django 4.1.5 on 2023-06-10 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0012_bikestatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='bike',
            name='latitude',
            field=models.FloatField(default=52.2377),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bike',
            name='longitude',
            field=models.FloatField(default=20.9912),
            preserve_default=False,
        ),
    ]
