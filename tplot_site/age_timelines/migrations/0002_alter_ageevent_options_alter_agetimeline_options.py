# Generated by Django 4.2.3 on 2023-08-06 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('age_timelines', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ageevent',
            options={'ordering': ['start_year', 'start_month']},
        ),
        migrations.AlterModelOptions(
            name='agetimeline',
            options={'ordering': ['title']},
        ),
    ]
