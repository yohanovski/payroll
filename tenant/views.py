from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import TenantCreationForm, TenantInfoForm
from .models import Tenant, TenantInfo
from audit.models import Audit, Monitoring  # Import des modèles d'audit et monitoring

# Superuser creates a tenant and is redirected to fill in tenant info, then to tenant list
@user_passes_test(lambda u: u.is_superuser)
def create_tenant(request):
    if request.method == 'POST':
        form = TenantCreationForm(request.POST)
        if form.is_valid():
            tenant = form.save()  # Create the tenant
            # Enregistrer l'action dans l'audit
            Audit.objects.create(
                user=request.user,
                tenant=tenant,
                table_name='Tenant',
                row_id=tenant.id,
                column_name='All',
                old_value='',
                new_value=str(tenant),
                change_date=timezone.now()
            )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=tenant,
                activity='Tenant Created',
                description=f'Tenant {tenant.name} was created',
                timestamp=timezone.now()
            )
            return redirect('create-tenant-info', tenant_id=tenant.id)  # Redirect to tenant info form
    else:
        form = TenantCreationForm()
    return render(request, 'tenant/create_tenant.html', {'form': form})

# Superuser fills tenant info after creating the tenant
@user_passes_test(lambda u: u.is_superuser)
def create_tenant_info(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantInfoForm(request.POST)
        if form.is_valid():
            tenant_info = form.save(commit=False)
            tenant_info.tenant = tenant  # Link the tenant info to the tenant
            tenant_info.save()
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=tenant,
                activity='Tenant Info Created',
                description=f'Info for Tenant {tenant.name} was created',
                timestamp=timezone.now()
            )
            return redirect('tenant-list')  # Redirect to tenant list after saving info
    else:
        form = TenantInfoForm()
    return render(request, 'tenant/create_tenant_info.html', {'form': form, 'tenant': tenant})

# Superuser updates tenant info
@user_passes_test(lambda u: u.is_superuser)
def update_tenant_info(request, tenant_id):
    tenant_info = get_object_or_404(TenantInfo, tenant__id=tenant_id)
    old_tenant_info = tenant_info.__dict__.copy()  # Sauvegarder l'état avant la mise à jour
    if request.method == 'POST':
        form = TenantInfoForm(request.POST, instance=tenant_info)
        if form.is_valid():
            form.save()
            # Comparer les anciennes et nouvelles données pour l'audit
            for field in form.changed_data:
                old_value = old_tenant_info[field]
                new_value = getattr(tenant_info, field)
                Audit.objects.create(
                    user=request.user,
                    tenant=tenant_info.tenant,
                    table_name='TenantInfo',
                    row_id=tenant_info.id,
                    column_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    change_date=timezone.now()
                )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=tenant_info.tenant,
                activity='Tenant Info Updated',
                description=f'Info for Tenant {tenant_info.tenant.name} was updated',
                timestamp=timezone.now()
            )
            return redirect('tenant-list')
    else:
        form = TenantInfoForm(instance=tenant_info)
    return render(request, 'tenant/update_tenant_info.html', {'form': form})

# Admin or member views their tenant info
@user_passes_test(lambda u: u.role in ['admin', 'member'])
def view_tenant_info(request):
    tenant_info = get_object_or_404(TenantInfo, tenant=request.user.tenant)
    # Enregistrer dans le monitoring
    Monitoring.objects.create(
        user=request.user,
        tenant=request.user.tenant,
        activity='Tenant Info Viewed',
        description=f'{request.user.email} viewed info for Tenant {tenant_info.tenant.name}',
        timestamp=timezone.now()
    )
    return render(request, 'tenant/view_tenant_info.html', {'tenant_info': tenant_info})

# Superuser lists all tenants
@user_passes_test(lambda u: u.is_superuser)
def tenant_list(request):
    tenants = Tenant.objects.all()
    # Enregistrer dans le monitoring
    Monitoring.objects.create(
        user=request.user,
        tenant=None,  # Pas de tenant spécifique
        activity='Tenant List Viewed',
        description='Superadmin viewed the tenant list',
        timestamp=timezone.now()
    )
    return render(request, 'tenant/tenant_list.html', {'tenants': tenants})

# Superuser updates a tenant
@user_passes_test(lambda u: u.is_superuser)
def update_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    old_tenant = tenant.__dict__.copy()  # Sauvegarder l'état avant la mise à jour
    if request.method == 'POST':
        form = TenantCreationForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            # Comparer les anciennes et nouvelles données pour l'audit
            for field in form.changed_data:
                old_value = old_tenant[field]
                new_value = getattr(tenant, field)
                Audit.objects.create(
                    user=request.user,
                    tenant=tenant,
                    table_name='Tenant',
                    row_id=tenant.id,
                    column_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    change_date=timezone.now()
                )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=tenant,
                activity='Tenant Updated',
                description=f'Tenant {tenant.name} was updated',
                timestamp=timezone.now()
            )
            return redirect('tenant-list')
    else:
        form = TenantCreationForm(instance=tenant)
    return render(request, 'tenant/update_tenant.html', {'form': form})

# Superuser deletes a tenant
@user_passes_test(lambda u: u.is_superuser)
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        # Enregistrer l'action dans l'audit avant la suppression
        Audit.objects.create(
            user=request.user,
            tenant=tenant,
            table_name='Tenant',
            row_id=tenant.id,
            column_name='All',
            old_value=str(tenant),
            new_value='Deleted',
            change_date=timezone.now()
        )
        tenant.delete()
        # Enregistrer dans le monitoring
        Monitoring.objects.create(
            user=request.user,
            tenant=tenant,
            activity='Tenant Deleted',
            description=f'Tenant {tenant.name} was deleted',
            timestamp=timezone.now()
        )
        return redirect('tenant-list')
    return render(request, 'tenant/confirm_delete.html', {'tenant': tenant})
