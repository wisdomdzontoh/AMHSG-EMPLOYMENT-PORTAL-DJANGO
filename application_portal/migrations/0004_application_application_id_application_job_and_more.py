# Generated by Django 5.1 on 2024-09-18 00:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_portal', '0003_rename_facilities_region_region_name_and_more'),
        ('jobs', '0003_alter_job_options_job_application_deadline_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_id',
            field=models.CharField(default='xxx', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jobs.job'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
