from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Paie, PaieDetail, EtatMonnaie
from .forms import PaieForm
from taux.models import TauxDeduction
from employe.models import Employe
from decimal import Decimal

# Vérifie si l'utilisateur est un membre ou un administrateur
def is_member_or_admin(user):
    return user.role in ['member', 'admin']

# Liste des paies (accessible aux membres et administrateurs)
@user_passes_test(is_member_or_admin)
def paie_list(request):
    paies = Paie.objects.filter(employe__tenant=request.user.tenant)
    return render(request, 'paie/paie_list.html', {'paies': paies})

# Création d'une paie (accessible uniquement aux membres)
@user_passes_test(lambda u: u.role == 'member')
def create_paie(request):
    if request.method == 'POST':
        form = PaieForm(request.POST)
        if form.is_valid():
            paie = form.save(commit=False)
            employe = form.cleaned_data['employe']
            paie.employe = employe
            paie.salaire_brut = Decimal(employe.TauxHoraire) * form.cleaned_data['nombre_heures']
            paie.salaire_net = paie.calculate_salaire_net()
            paie.save()

            taux_deductions = TauxDeduction.objects.filter(actif=True)
            for taux in taux_deductions:
                valeur_deduction = paie.salaire_brut * (taux.taux_actuel / 100)
                PaieDetail.objects.create(
                    paie=paie,
                    taux=taux,
                    valeur_taux=taux.taux_actuel,
                    valeur_deduction=valeur_deduction
                )

            etat_monnaie = EtatMonnaie.objects.create(paie=paie)
            etat_monnaie.calculate_etat_monnaie(paie.salaire_net)
            etat_monnaie.save()

            return redirect('paie-list')
    else:
        form = PaieForm()
    return render(request, 'paie/create_paie.html', {'form': form})

# Détails d'une paie (accessible aux membres et administrateurs)
@user_passes_test(is_member_or_admin)
def detail_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    paie_details = PaieDetail.objects.filter(paie=paie)
    etat_monnaie = get_object_or_404(EtatMonnaie, paie=paie)
    return render(request, 'paie/paie_detail.html', {
        'paie': paie,
        'paie_details': paie_details,
        'etat_monnaie': etat_monnaie
    })

# Modification d'une paie (accessible uniquement aux membres)
@user_passes_test(lambda u: u.role == 'member')
def edit_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    if request.method == 'POST':
        form = PaieForm(request.POST, instance=paie)
        if form.is_valid():
            paie = form.save(commit=False)
            paie.salaire_net = paie.calculate_salaire_net()
            paie.save()

            etat_monnaie = EtatMonnaie.objects.get(paie=paie)
            etat_monnaie.calculate_etat_monnaie(paie.salaire_net)
            etat_monnaie.save()

            return redirect('paie-list')
    else:
        form = PaieForm(instance=paie)
    return render(request, 'paie/update_paie.html', {'form': form})

# Suppression d'une paie (accessible uniquement aux membres)
@user_passes_test(lambda u: u.role == 'member')
def delete_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    paie.delete()
    return redirect('paie-list')
