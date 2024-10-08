# Generated by Django 5.0.6 on 2024-09-15 18:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('dateDeNaissance', models.DateField()),
                ('adresse', models.TextField()),
                ('ville', models.CharField(max_length=20)),
                ('CIN', models.CharField(max_length=10)),
                ('CNSS', models.CharField(max_length=50)),
                ('situationFamiliale', models.CharField(choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)'), ('divorce', 'Divorcé(e)')], default='celibataire', max_length=12)),
                ('nombreEnfants', models.IntegerField(default=0)),
                ('TauxHoraire', models.FloatField(default=0.0)),
                ('dateEntree', models.DateField()),
                ('dateSortie', models.DateField(blank=True, null=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tenant.tenant')),
            ],
            options={
                'verbose_name': 'Employe',
                'verbose_name_plural': 'Employes',
                'ordering': ['nom', 'prenom'],
            },
        ),
        migrations.CreateModel(
            name='Enfants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('dateDeNaissance', models.DateField()),
                ('isPermanent', models.BooleanField(default=False)),
                ('isEligible', models.BooleanField(default=True)),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employe.employe')),
            ],
            options={
                'verbose_name': 'enfant',
                'verbose_name_plural': 'enfants',
                'ordering': ['nom'],
            },
        ),
    ]
