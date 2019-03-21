# Generated by Django 2.1.5 on 2019-03-21 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unesco', '0002_remove_site_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='area_hectares',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='justification',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='site',
            name='year',
            field=models.IntegerField(null=True),
        ),
    ]
