from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from .models import TauxDeduction, TauxDeductionHistorique
from .forms import TauxDeductionForm
from tenant.models import Tenant
from audit.models import Monitoring, Audit

# Vérifier si l'utilisateur est un membre du tenant
def is_member(user):
    return user.role == 'member'

# Superadmin peut visualiser les taux d'un tenant
@user_passes_test(lambda u: u.is_superuser)
def view_taux_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    taux = TauxDeduction.objects.filter(tenant=tenant)
    return render(request, 'taux/view_taux_tenant.html', {'taux': taux, 'tenant': tenant})

# Liste des taux (accessible aux membres)
@user_passes_test(is_member)
def taux_list(request):
    taux = TauxDeduction.objects.filter(tenant=request.user.tenant)
    return render(request, 'taux/taux_list.html', {'taux': taux})

# Création d'un taux (membre)
@user_passes_test(is_member)
def create_taux(request):
    if request.method == 'POST':
        form = TauxDeductionForm(request.POST)
        if form.is_valid():
            taux = form.save(commit=False)
            taux.tenant = request.user.tenant
            taux.save()

            # Enregistrer dans l'historique
            TauxDeductionHistorique.objects.create(
                taux=taux,
                newTaux=taux.taux_actuel,
                date_debut=taux.date_debut
            )

            # Monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                activity='Taux Created',
                description=f'Taux {taux.nom} créé avec un taux de {taux.taux_actuel}%',
                timestamp=timezone.now()
            )

            return redirect('taux-list')
    else:
        form = TauxDeductionForm()
    return render(request, 'taux/create_taux.html', {'form': form})

# Mise à jour d'un taux (membre)
@user_passes_test(is_member)
def update_taux(request, taux_id):
    taux = get_object_or_404(TauxDeduction, id=taux_id, tenant=request.user.tenant)
    old_taux = taux.taux_actuel  # Sauvegarder l'ancienne valeur pour l'historique
    if request.method == 'POST':
        form = TauxDeductionForm(request.POST, instance=taux)
        if form.is_valid():
            taux = form.save()

            # Enregistrer dans l'historique
            TauxDeductionHistorique.objects.create(
                taux=taux,
                newTaux=taux.taux_actuel,
                date_debut=taux.date_debut
            )

            # Audit et Monitoring
            Audit.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                table_name='TauxDeduction',
                row_id=taux.id,
                column_name='taux_actuel',
                old_value=str(old_taux),
                new_value=str(taux.taux_actuel),
                change_date=timezone.now()
            )

            Monitoring.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                activity='Taux Updated',
                description=f'Taux {taux.nom} mis à jour à {taux.taux_actuel}%',
                timestamp=timezone.now()
            )

            return redirect('taux-list')
    else:
        form = TauxDeductionForm(instance=taux)
    return render(request, 'taux/update_taux.html', {'form': form})

# Suppression d'un taux (membre)
@user_passes_test(is_member)
def delete_taux(request, taux_id):
    taux = get_object_or_404(TauxDeduction, id=taux_id, tenant=request.user.tenant)
    if request.method == 'POST':
        # Enregistrer l'action dans l'audit avant la suppression
        Audit.objects.create(
            user=request.user,
            tenant=request.user.tenant,
            table_name='TauxDeduction',
            row_id=taux.id,
            column_name='All',
            old_value=str(taux),
            new_value='Deleted',
            change_date=timezone.now()
        )

        taux.delete()

        # Monitoring
        Monitoring.objects.create(
            user=request.user,
            tenant=request.user.tenant,
            activity='Taux Deleted',
            description=f'Taux {taux.nom} supprimé',
            timestamp=timezone.now()
        )

        return redirect('taux-list')
    return render(request, 'taux/confirm_delete_taux.html', {'taux': taux})
