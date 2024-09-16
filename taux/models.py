from django.db import models
from django.utils import timezone

class TauxDeduction(models.Model):
    nom = models.CharField(max_length=100)  
    taux_actuel = models.DecimalField(max_digits=5, decimal_places=2)  
    date_debut = models.DateField(default=timezone.now)  
    actif = models.BooleanField(default=True)  # Indique si le taux est encore en vigueur

    def __str__(self):
        return f"{self.nom} ({self.taux_actuel}%)"

    class Meta:
        verbose_name = "Taux de Déduction"
        verbose_name_plural = "Taux de Déduction"
        ordering = ['nom', 'date_debut']

class TauxDeductionHistorique(models.Model):
    taux = models.ForeignKey(TauxDeduction, on_delete=models.CASCADE, related_name='historique')
    newTaux = models.DecimalField(max_digits=5, decimal_places=2)  
    date_debut = models.DateField()

    def __str__(self):
        return f"Historique pour {self.taux.nom} - Nouveau Taux: {self.newTaux}%"

    class Meta:
        verbose_name = "Historique du Taux de Déduction"
        verbose_name_plural = "Historiques des Taux de Déduction"
        ordering = ['taux', 'date_debut']
