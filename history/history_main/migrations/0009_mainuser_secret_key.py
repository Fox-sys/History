# Generated by Django 3.1.5 on 2021-02-06 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history_main', '0008_auto_20210129_0618'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainuser',
            name='secret_key',
            field=models.CharField(default='ZHrfSVZpQAsydOxceMDp', max_length=20),
        ),
    ]