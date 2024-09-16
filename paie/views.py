from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Paie, PaieDetail, EtatMonnaie
from .forms import PaieForm
from taux.models import TauxDeduction
from employe.models import Employe

def is_member(user):
    return user.role == 'member'


def paie_list(request):
    paies = Paie.objects.filter(employe__tenant=request.user.tenant)
    return render(request, 'paie/paie_list.html', {'paies': paies})


@user_passes_test(is_member)
def create_paie(request):
    if request.method == 'POST':
        form = PaieForm(request.POST)
        if form.is_valid():
            paie = form.save(commit=False)
            employe = Employe.objects.get(id=form.cleaned_data['employe'])
            paie.salaire_brut = employe.TauxHoraire * form.cleaned_data['nombre_heures']
            paie.salaire_net = paie.calculate_salaire_net()
            paie.save()

            for taux in TauxDeduction.objects.filter(actif=True):
                PaieDetail.objects.create(paie=paie, taux=taux, valeur_taux=taux.taux_actuel)

            # Create EtatMonnaie and calculate based on salaire_net
            etat_monnaie = EtatMonnaie.objects.create(paie=paie)
            etat_monnaie.calculate_etat_monnaie(paie.salaire_net)
            etat_monnaie.save()

            return redirect('paie-list')
    else:
        form = PaieForm()
    return render(request, 'paie/create_paie.html', {'form': form})


@user_passes_test(is_member)
def detail_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    paie_details = PaieDetail.objects.filter(paie=paie)
    etat_monnaie = get_object_or_404(EtatMonnaie, paie=paie)
    return render(request, 'paie/paie_detail.html', {'paie': paie, 'paie_details': paie_details, 'etat_monnaie': etat_monnaie})


@user_passes_test(is_member)
def edit_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    if request.method == 'POST':
        form = PaieForm(request.POST, instance=paie)
        if form.is_valid():
            paie = form.save(commit=False)
            paie.salaire_net = paie.calculate_salaire_net()
            paie.save()

            # Update EtatMonnaie
            etat_monnaie = EtatMonnaie.objects.get(paie=paie)
            etat_monnaie.calculate_etat_monnaie(paie.salaire_net)
            etat_monnaie.save()

            return redirect('paie-list')
    else:
        form = PaieForm(instance=paie)
    return render(request, 'paie/update_paie.html', {'form': form})


@user_passes_test(is_member)
def delete_paie(request, paie_id):
    paie = get_object_or_404(Paie, id=paie_id)
    paie.delete()
    return redirect('paie-list')
