# Generated by Django 3.1.2 on 2020-10-15 12:24

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='otherpage',
            managers=[
                ('objects_excluding_bins', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='testpage',
            managers=[
                ('objects_excluding_bins', django.db.models.manager.Manager()),
            ],
        ),
    ]