from django.db import models
from employe.models import Employe
from taux.models import TauxDeduction
from django.utils import timezone

class Paie(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    nombre_heures = models.DecimalField(max_digits=5, decimal_places=2)
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2)
    salaire_net = models.DecimalField(max_digits=10, decimal_places=2)
    date_paie = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Paie pour {self.employe.nom} - {self.date_paie}"

    def calculate_salaire_net(self):
        # Calculer le salaire net en appliquant les taux de déduction
        taux_deductions = TauxDeduction.objects.filter(actif=True)
        deduction_total = sum([taux.taux_actuel for taux in taux_deductions])
        salaire_net = self.salaire_brut * (1 - deduction_total / 100)
        return salaire_net


class PaieDetail(models.Model):
    paie = models.ForeignKey(Paie, on_delete=models.CASCADE, related_name='details')
    taux = models.ForeignKey(TauxDeduction, on_delete=models.CASCADE)
    valeur_taux = models.DecimalField(max_digits=5, decimal_places=2)


class EtatMonnaie(models.Model):
    paie = models.OneToOneField(Paie, on_delete=models.CASCADE)
    N200 = models.IntegerField(default=0)
    N100 = models.IntegerField(default=0)
    N50 = models.IntegerField(default=0)
    N20 = models.IntegerField(default=0)
    N10 = models.IntegerField(default=0)
    N5 = models.IntegerField(default=0)
    N2 = models.IntegerField(default=0)
    N1 = models.IntegerField(default=0)
    N050 = models.IntegerField(default=0)
    N020 = models.IntegerField(default=0)
    N010 = models.IntegerField(default=0)

    def __str__(self):
        return f"État de Monnaie pour la paie de {self.paie.employe.nom}"

    def calculate_etat_monnaie(self, salaire_net):
        self.N200 = salaire_net // 200
        salaire_net %= 200
        self.N100 = salaire_net // 100
        salaire_net %= 100
        self.N50 = salaire_net // 50
        salaire_net %= 50
        self.N20 = salaire_net // 20
        salaire_net %= 20
        self.N10 = salaire_net // 10
        salaire_net %= 10
        self.N5 = salaire_net // 5
        salaire_net %= 5
        self.N2 = salaire_net // 2
        salaire_net %= 2
        self.N1 = salaire_net // 1
        salaire_net %= 1
        self.N050 = salaire_net // 0.5
        salaire_net %= 0.5
        self.N020 = salaire_net // 0.2
        salaire_net %= 0.2
        self.N010 = salaire_net // 0.1
        salaire_net %= 0.1
