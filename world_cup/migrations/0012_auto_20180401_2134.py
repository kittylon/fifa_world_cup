# Generated by Django 2.0.1 on 2018-04-02 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world_cup', '0011_auto_20180401_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='emoji',
            field=models.CharField(default=' ', max_length=255),
        ),
        migrations.AlterField(
            model_name='userteam',
            name='emoji',
            field=models.CharField(default=' ', max_length=255),
        ),
    ]
