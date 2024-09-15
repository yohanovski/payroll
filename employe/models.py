from django.db import models
from tenant.models import Tenant  # Import Tenant model

class Employe(models.Model):
    SITUATION_FAMILIALE_CHOICES = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('divorce', 'Divorcé(e)'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)  # Association with Tenant
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    dateDeNaissance = models.DateField()
    adresse = models.TextField()
    ville = models.CharField(max_length=20)
    CIN = models.CharField(max_length=10)
    CNSS = models.CharField(max_length=50)
    situationFamiliale = models.CharField(max_length=12, choices=SITUATION_FAMILIALE_CHOICES, default='celibataire')
    nombreEnfants = models.IntegerField(default=0)
    TauxHoraire = models.FloatField(default=0.0)
    dateEntree = models.DateField()
    dateSortie = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    class Meta: 
        verbose_name = "Employe"
        verbose_name_plural = "Employes"
        ordering = ['nom', 'prenom']


class Enfants(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    dateDeNaissance = models.DateField()
    isPermanent = models.BooleanField(default=False)
    isEligible = models.BooleanField(default=True)  # New attribute

    def __str__(self):
        permanence = "permanent" if self.isPermanent else "non-permanent"
        eligibility = "eligible" if self.isEligible else "not eligible"
        return f"{self.prenom} (enfant de {self.employe.nom} {self.employe.prenom}) est {permanence} et {eligibility}"
    
    class Meta: 
        verbose_name = "enfant"
        verbose_name_plural = "enfants"
        ordering = ['nom']
