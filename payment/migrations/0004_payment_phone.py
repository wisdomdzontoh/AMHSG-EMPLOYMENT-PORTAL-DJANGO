# Generated by Django 5.1 on 2024-09-28 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_payment_job'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='phone',
            field=models.CharField(default='0558749735', max_length=50),
        ),
    ]
