# Generated by Django 4.2.4 on 2024-08-25 20:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("timelines", "0003_tag_description_tag_display"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventarea",
            name="weight",
            field=models.PositiveSmallIntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
