# Generated by Django 2.0.12 on 2019-06-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingest', '0009_auto_20190626_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenda',
            name='cutoff_time',
            field=models.PositiveIntegerField(default=1561535880.878893),
        ),
        migrations.AlterField(
            model_name='agenda',
            name='pdf_time',
            field=models.PositiveIntegerField(default=1561535880.878942),
        ),
    ]
