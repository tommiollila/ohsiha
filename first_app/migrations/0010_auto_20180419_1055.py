# Generated by Django 2.0.2 on 2018-04-19 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0009_auto_20180419_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='DegreeCoordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_coo', models.CharField(default='', max_length=25)),
                ('y_coo', models.CharField(default='', max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='trafficlightdetectors',
            name='x_coo',
        ),
        migrations.RemoveField(
            model_name='trafficlightdetectors',
            name='y_coo',
        ),
    ]
