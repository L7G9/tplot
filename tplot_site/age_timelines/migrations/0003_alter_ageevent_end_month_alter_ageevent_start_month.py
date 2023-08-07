# Generated by Django 4.2.3 on 2023-08-06 12:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('age_timelines', '0002_alter_ageevent_options_alter_agetimeline_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ageevent',
            name='end_month',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(11), django.core.validators.MinValueValidator(-11)]),
        ),
        migrations.AlterField(
            model_name='ageevent',
            name='start_month',
            field=models.SmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(11), django.core.validators.MinValueValidator(-11)]),
        ),
    ]