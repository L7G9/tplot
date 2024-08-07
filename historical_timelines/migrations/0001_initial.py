# Generated by Django 4.2.4 on 2024-07-25 21:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("timelines", "0002_rename_timeline_area_event_event_area"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalTimeline",
            fields=[
                (
                    "timeline_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="timelines.timeline",
                    ),
                ),
                (
                    "scale_unit",
                    models.IntegerField(
                        choices=[
                            (1, "1 Years"),
                            (5, "5 Years"),
                            (10, "10 Years"),
                            (25, "25 Years"),
                            (50, "50 Years"),
                            (100, "100 Years"),
                            (500, "500 Years"),
                            (1000, "1000 Years"),
                        ],
                        default=10,
                    ),
                ),
            ],
            options={
                "ordering": ["title"],
            },
            bases=("timelines.timeline",),
        ),
        migrations.CreateModel(
            name="HistoricalEvent",
            fields=[
                (
                    "event_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="timelines.event",
                    ),
                ),
                (
                    "start_bc_ad",
                    models.SmallIntegerField(
                        choices=[(-1, "BC"), (1, "AD")], default=-1
                    ),
                ),
                (
                    "start_year",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                    ),
                ),
                (
                    "end_bc_ad",
                    models.SmallIntegerField(
                        choices=[(-1, "BC"), (1, "AD")], default=-1
                    ),
                ),
                (
                    "end_year",
                    models.PositiveIntegerField(
                        default=1,
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                    ),
                ),
                (
                    "historical_timeline",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="historical_timelines.historicaltimeline",
                    ),
                ),
            ],
            options={
                "ordering": [
                    django.db.models.expressions.CombinedExpression(
                        models.F("start_bc_ad"), "*", models.F("start_year")
                    )
                ],
            },
            bases=("timelines.event",),
        ),
    ]
