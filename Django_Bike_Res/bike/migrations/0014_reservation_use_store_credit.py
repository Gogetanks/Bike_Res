# Generated by Django 4.1.5 on 2023-06-10 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0013_bike_latitude_bike_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='use_store_credit',
            field=models.BooleanField(default=False),
        ),
    ]
