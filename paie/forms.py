from django import forms
from .models import Paie, EtatMonnaie
from employe.models import Employe

class PaieForm(forms.ModelForm):
    employe = forms.ModelChoiceField(queryset=Employe.objects.all(), label="Employé", required=True)
    nombre_heures = forms.DecimalField(max_digits=5, decimal_places=2, label="Nombre d'heures travaillées", required=True)

    class Meta:
        model = Paie
        fields = ['employe', 'nombre_heures']

class EtatMonnaieForm(forms.ModelForm):
    N200 = forms.IntegerField(label="200 MAD", required=False)
    N100 = forms.IntegerField(label="100 MAD", required=False)
    N50 = forms.IntegerField(label="50 MAD", required=False)
    N20 = forms.IntegerField(label="20 MAD", required=False)
    N10 = forms.IntegerField(label="10 MAD", required=False)
    N5 = forms.IntegerField(label="5 MAD", required=False)
    N2 = forms.IntegerField(label="2 MAD", required=False)
    N1 = forms.IntegerField(label="1 MAD", required=False)
    N050 = forms.IntegerField(label="0.50 MAD", required=False)
    N020 = forms.IntegerField(label="0.20 MAD", required=False)
    N010 = forms.IntegerField(label="0.10 MAD", required=False)

    class Meta:
        model = EtatMonnaie
        fields = ['N200', 'N100', 'N50', 'N20', 'N10', 'N5', 'N2', 'N1', 'N050', 'N020', 'N010']
