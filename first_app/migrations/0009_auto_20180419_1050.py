# Generated by Django 2.0.2 on 2018-04-19 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0008_auto_20180419_1048'),
    ]

    operations = [
        migrations.AddField(
            model_name='trafficlightdetectors',
            name='latitude',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='trafficlightdetectors',
            name='longitude',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
