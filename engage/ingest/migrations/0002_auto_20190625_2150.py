# Generated by Django 2.0.12 on 2019-06-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='cutoff_time',
            field=models.PositiveIntegerField(default=1561499412.017618),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='pdf_time',
            field=models.PositiveIntegerField(default=1561499412.017685),
        ),
    ]
