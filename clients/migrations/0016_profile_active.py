# Generated by Django 2.0.1 on 2018-04-17 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_client_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]