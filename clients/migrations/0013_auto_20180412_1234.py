# Generated by Django 2.0.1 on 2018-04-12 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0012_auto_20180412_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='document_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]