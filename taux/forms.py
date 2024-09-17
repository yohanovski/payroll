from django import forms
from .models import TauxDeduction

class TauxDeductionForm(forms.ModelForm):
    class Meta:
        model = TauxDeduction
        fields = ['nom', 'taux_actuel', 'date_debut', 'actif']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_actuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nom': 'Nom du Taux',
            'taux_actuel': 'Taux Actuel (%)',
            'date_debut': 'Date de Début',
            'actif': 'Taux encore pris en compte ?',
        }
