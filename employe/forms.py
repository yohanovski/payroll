# employe/forms.py
from django import forms
from .models import Employe, Enfants

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'dateDeNaissance', 'adresse', 'ville', 'CIN', 'CNSS', 'situationFamiliale', 'nombreEnfants', 'TauxHoraire', 'dateEntree', 'dateSortie']

class EnfantForm(forms.ModelForm):
    class Meta:
        model = Enfants
        fields = ['nom', 'prenom', 'dateDeNaissance', 'isPermanent', 'isEligible']
