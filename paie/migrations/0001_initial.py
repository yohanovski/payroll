# Generated by Django 5.0.6 on 2024-09-16 13:38

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employe', '0001_initial'),
        ('taux', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_heures', models.DecimalField(decimal_places=2, max_digits=5)),
                ('salaire_brut', models.DecimalField(decimal_places=2, max_digits=10)),
                ('salaire_net', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_paie', models.DateField(default=django.utils.timezone.now)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.employe')),
            ],
        ),
        migrations.CreateModel(
            name='EtatMonnaie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('N200', models.IntegerField(default=0)),
                ('N100', models.IntegerField(default=0)),
                ('N50', models.IntegerField(default=0)),
                ('N20', models.IntegerField(default=0)),
                ('N10', models.IntegerField(default=0)),
                ('N5', models.IntegerField(default=0)),
                ('N2', models.IntegerField(default=0)),
                ('N1', models.IntegerField(default=0)),
                ('N050', models.IntegerField(default=0)),
                ('N020', models.IntegerField(default=0)),
                ('N010', models.IntegerField(default=0)),
                ('paie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paie.paie')),
            ],
        ),
        migrations.CreateModel(
            name='PaieDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur_taux', models.DecimalField(decimal_places=2, max_digits=5)),
                ('paie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='paie.paie')),
                ('taux', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taux.tauxdeduction')),
            ],
        ),
    ]
