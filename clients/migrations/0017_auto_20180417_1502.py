# Generated by Django 2.0.1 on 2018-04-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0016_profile_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='nit',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
