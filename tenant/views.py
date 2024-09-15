from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import TenantCreationForm, TenantInfoForm
from .models import Tenant, TenantInfo

# Superuser creates a tenant and is redirected to fill in tenant info, then to tenant list
@user_passes_test(lambda u: u.is_superuser)
def create_tenant(request):
    if request.method == 'POST':
        form = TenantCreationForm(request.POST)
        if form.is_valid():
            tenant = form.save()  # Create the tenant
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
            return redirect('tenant-list')  # Redirect to tenant list after saving info
    else:
        form = TenantInfoForm()
    return render(request, 'tenant/create_tenant_info.html', {'form': form, 'tenant': tenant})

# Superuser updates tenant info
@user_passes_test(lambda u: u.is_superuser)
def update_tenant_info(request, tenant_id):
    tenant_info = get_object_or_404(TenantInfo, tenant__id=tenant_id)
    if request.method == 'POST':
        form = TenantInfoForm(request.POST, instance=tenant_info)
        if form.is_valid():
            form.save()
            return redirect('tenant-list')
    else:
        form = TenantInfoForm(instance=tenant_info)
    return render(request, 'tenant/update_tenant_info.html', {'form': form})

# Admin or member views their tenant info
@user_passes_test(lambda u: u.role in ['admin', 'member'])
def view_tenant_info(request):
    tenant_info = get_object_or_404(TenantInfo, tenant=request.user.tenant)
    return render(request, 'tenant/view_tenant_info.html', {'tenant_info': tenant_info})

# Superuser lists all tenants
@user_passes_test(lambda u: u.is_superuser)
def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'tenant/tenant_list.html', {'tenants': tenants})

# Superuser updates a tenant
@user_passes_test(lambda u: u.is_superuser)
def update_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        form = TenantCreationForm(request.POST, instance=tenant)
        if form.is_valid():
            form.save()
            return redirect('tenant-list')  # Redirect to updated tenant list after update
    else:
        form = TenantCreationForm(instance=tenant)
    return render(request, 'tenant/update_tenant.html', {'form': form})

# Superuser deletes a tenant
@user_passes_test(lambda u: u.is_superuser)
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    tenant.delete()
    return redirect('tenant-list')  # Redirect to updated tenant list after deletion
