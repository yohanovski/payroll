# Generated by Django 5.0.6 on 2024-09-17 20:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taux', '0001_initial'),
        ('tenant', '0002_alter_tenantinfo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tauxdeduction',
            name='tenant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant'),
        ),
    ]
