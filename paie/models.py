from django.db import models
from employe.models import Employe
from taux.models import TauxDeduction
from django.utils import timezone
from decimal import Decimal

class Paie(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    nombre_heures = models.DecimalField(max_digits=5, decimal_places=2)
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2)
    salaire_net = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date_paie = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Paie pour {self.employe.nom} - {self.date_paie}"

    def calculate_salaire_net(self):
        taux_deductions = TauxDeduction.objects.filter(actif=True)
        deduction_total = Decimal(0)
        for taux in taux_deductions:
            deduction = self.salaire_brut * (taux.taux_actuel / 100)
            deduction_total += deduction
            # PaieDetail is created in the view after saving the Paie object.
        salaire_net = self.salaire_brut - deduction_total
        return salaire_net

class PaieDetail(models.Model):
    paie = models.ForeignKey(Paie, on_delete=models.CASCADE, related_name='details')
    taux = models.ForeignKey(TauxDeduction, on_delete=models.CASCADE)
    valeur_taux = models.DecimalField(max_digits=5, decimal_places=2)
    valeur_deduction = models.DecimalField(max_digits=10, decimal_places=2, null=True)

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
        salaire_net = Decimal(salaire_net)
        self.N200 = int(salaire_net // 200)
        salaire_net %= 200
        self.N100 = int(salaire_net // 100)
        salaire_net %= 100
        self.N50 = int(salaire_net // 50)
        salaire_net %= 50
        self.N20 = int(salaire_net // 20)
        salaire_net %= 20
        self.N10 = int(salaire_net // 10)
        salaire_net %= 10
        self.N5 = int(salaire_net // 5)
        salaire_net %= 5
        self.N2 = int(salaire_net // 2)
        salaire_net %= 2
        self.N1 = int(salaire_net // 1)
        salaire_net %= 1
        self.N050 = int(salaire_net // Decimal('0.5'))
        salaire_net %= Decimal('0.5')
        self.N020 = int(salaire_net // Decimal('0.2'))
        salaire_net %= Decimal('0.2')
        self.N010 = int(salaire_net // Decimal('0.1'))
        salaire_net %= Decimal('0.1')
