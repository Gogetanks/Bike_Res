# Generated by Django 4.1.5 on 2023-05-14 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0008_alter_user_credit'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='categories/'),
            preserve_default=False,
        ),
    ]
