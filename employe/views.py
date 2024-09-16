from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import EmployeForm, EnfantForm
from .models import Employe, Enfants
from tenant.models import Tenant
from audit.models import Audit, Monitoring  # Import des modèles d'audit et monitoring

# Check if user is admin or member
def is_admin_or_member(user):
    return user.role in ['admin', 'member']

# List employees (accessible by admin or member)
@user_passes_test(is_admin_or_member)
def employe_list(request):
    employes = Employe.objects.filter(tenant=request.user.tenant)  # Filter employees by tenant
    Monitoring.objects.create(
        user=request.user,
        tenant=request.user.tenant,
        activity='Employee List Viewed',
        description='User viewed the employee list',
        timestamp=timezone.now()
    )
    return render(request, 'employe/employe_list.html', {'employes': employes})

# Create an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def create_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            employe = form.save(commit=False)
            employe.tenant = request.user.tenant  # Assign the current user's tenant
            employe.save()
            # Enregistrer l'action dans l'audit
            Audit.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                table_name='Employe',
                row_id=employe.id,
                column_name='All',
                old_value='',
                new_value=str(employe),
                change_date=timezone.now()
            )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                activity='Employee Created',
                description=f'Employee {employe.nom} {employe.prenom} was created',
                timestamp=timezone.now()
            )
            return redirect('employe-list')
    else:
        form = EmployeForm()
    return render(request, 'employe/create_employe.html', {'form': form})

# Update an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def update_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    old_employe = employe.__dict__.copy()  # Sauvegarder l'état avant la mise à jour
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            employe = form.save()
            # Comparer les anciennes et nouvelles données pour l'audit
            for field in form.changed_data:
                old_value = old_employe[field]
                new_value = getattr(employe, field)
                Audit.objects.create(
                    user=request.user,
                    tenant=request.user.tenant,
                    table_name='Employe',
                    row_id=employe.id,
                    column_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    change_date=timezone.now()
                )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                activity='Employee Updated',
                description=f'Employee {employe.nom} {employe.prenom} was updated',
                timestamp=timezone.now()
            )
            return redirect('employe-list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'employe/update_employe.html', {'form': form})

# Delete an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def delete_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    if request.method == 'POST':
        # Enregistrer l'action dans l'audit avant la suppression
        Audit.objects.create(
            user=request.user,
            tenant=request.user.tenant,
            table_name='Employe',
            row_id=employe.id,
            column_name='All',
            old_value=str(employe),
            new_value='Deleted',
            change_date=timezone.now()
        )
        employe.delete()
        # Enregistrer dans le monitoring
        Monitoring.objects.create(
            user=request.user,
            tenant=request.user.tenant,
            activity='Employee Deleted',
            description=f'Employee {employe.nom} {employe.prenom} was deleted',
            timestamp=timezone.now()
        )
        return redirect('employe-list')
    return render(request, 'employe/confirm_delete.html', {'employe': employe})

# View employee details
@user_passes_test(is_admin_or_member)
def employe_detail(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    enfants = Enfants.objects.filter(employe=employe)
    Monitoring.objects.create(
        user=request.user,
        tenant=request.user.tenant,
        activity='Employee Detail Viewed',
        description=f'User viewed details for employee {employe.nom} {employe.prenom}',
        timestamp=timezone.now()
    )
    return render(request, 'employe/employe_detail.html', {'employe': employe, 'enfants': enfants})

# Create an enfant for an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def create_enfant(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    if request.method == 'POST':
        form = EnfantForm(request.POST)
        if form.is_valid():
            enfant = form.save(commit=False)
            enfant.employe = employe
            enfant.save()
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=request.user.tenant,
                activity='Child Created',
                description=f'Child {enfant.nom} {enfant.prenom} was created for employee {employe.nom} {employe.prenom}',
                timestamp=timezone.now()
            )
            return redirect('employe-detail', employe_id=employe.id)
    else:
        form = EnfantForm()
    return render(request, 'employe/create_enfant.html', {'form': form, 'employe': employe})

# Update an enfant (only admin or member)
@user_passes_test(is_admin_or_member)
def update_enfant(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    old_enfant = enfant.__dict__.copy()  # Sauvegarder l'état avant la mise à jour
    if request.method == 'POST':
        form = EnfantForm(request.POST, instance=enfant)
        if form.is_valid():
            enfant = form.save()
            # Comparer les anciennes et les nouvelles données pour l'audit
            for field in form.changed_data:
                old_value = old_enfant[field]
                new_value = getattr(enfant, field)
                Audit.objects.create(
                    user=request.user,
                    tenant=enfant.employe.tenant,
                    table_name='Enfants',
                    row_id=enfant.id,
                    column_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    change_date=timezone.now()
                )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=enfant.employe.tenant,
                activity='Child Updated',
                description=f'Child {enfant.nom} {enfant.prenom} was updated',
                timestamp=timezone.now()
            )
            return redirect('employe-detail', employe_id=enfant.employe.id)
    else:
        form = EnfantForm(instance=enfant)
    return render(request, 'employe/update_enfant.html', {'form': form})

# Delete an enfant (only admin or member)
@user_passes_test(is_admin_or_member)
def delete_enfant(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    employe_id = enfant.employe.id
    if request.method == 'POST':
        # Enregistrer l'action dans l'audit avant la suppression
        Audit.objects.create(
            user=request.user,
            tenant=enfant.employe.tenant,
            table_name='Enfants',
            row_id=enfant.id,
            column_name='All',
            old_value=str(enfant),
            new_value='Deleted',
            change_date=timezone.now()
        )
        enfant.delete()
        # Enregistrer dans le monitoring
        Monitoring.objects.create(
            user=request.user,
            tenant=enfant.employe.tenant,
            activity='Child Deleted',
            description=f'Child {enfant.nom} {enfant.prenom} was deleted',
            timestamp=timezone.now()
        )
        return redirect('employe-detail', employe_id=employe_id)
    return render(request, 'employe/confirm_delete.html', {'enfant': enfant})

# View enfant details
@user_passes_test(is_admin_or_member)
def enfant_detail(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    Monitoring.objects.create(
        user=request.user,
        tenant=request.user.tenant,
        activity='Child Detail Viewed',
        description=f'User viewed details for child {enfant.nom} {enfant.prenom}',
        timestamp=timezone.now()
    )
    return render(request, 'employe/enfant_detail.html', {'enfant': enfant})
