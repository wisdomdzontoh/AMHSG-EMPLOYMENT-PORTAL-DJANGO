# Generated by Django 5.1 on 2024-08-23 00:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),
    ]
