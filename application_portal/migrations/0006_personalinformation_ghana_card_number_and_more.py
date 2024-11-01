# Generated by Django 5.1 on 2024-09-19 08:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application_portal', '0005_application_professional_registration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalinformation',
            name='ghana_card_number',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AlterField(
            model_name='application',
            name='professional_registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application_portal.professionalregistration'),
        ),
    ]
