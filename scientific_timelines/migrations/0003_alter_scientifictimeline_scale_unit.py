# Generated by Django 4.2.4 on 2024-08-25 20:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scientific_timelines", "0002_alter_scientifictimeline_scale_unit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scientifictimeline",
            name="scale_unit",
            field=models.IntegerField(
                choices=[
                    (100, "0.1 Thousand Years"),
                    (500, "0.5 Thousand Years"),
                    (1000, "1 Thousand Years"),
                    (5000, "5 Thousand Years"),
                    (10000, "10 Thousand Years"),
                    (50000, "50 Thousand Years"),
                    (100000, "0.1 Million Years"),
                    (500000, "0.5 Million Years"),
                    (1000000, "1 Million Years"),
                    (5000000, "5 Million Years"),
                    (10000000, "10 Million Years"),
                    (50000000, "50 Million Years"),
                    (100000000, "0.1 Billion Years"),
                    (500000000, "0.5 Billion Years"),
                    (1000000000, "1 Billion Years"),
                ],
                default=1000,
            ),
        ),
    ]
