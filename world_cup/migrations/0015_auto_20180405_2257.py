# Generated by Django 2.0.1 on 2018-04-06 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world_cup', '0014_auto_20180405_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='realmatch',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='real_loser', to='world_cup.UserTeam'),
        ),
        migrations.AddField(
            model_name='realmatch',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='real_winner', to='world_cup.UserTeam'),
        ),
    ]