# Generated by Django 3.1.5 on 2021-01-29 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history_main', '0006_auto_20210128_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='avatar',
            field=models.ImageField(upload_to='user_avatars/'),
        ),
    ]
