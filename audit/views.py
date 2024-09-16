from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Audit, Monitoring
from users.models import CustomUser
from tenant.models import Tenant

# Check if user is superadmin
def is_superadmin(user):
    return user.role == 'superadmin'

# View audit logs (accessible only by superadmin)
@user_passes_test(is_superadmin)
def audit_list(request):
    audits = Audit.objects.all()

    # Filtering by role and tenant if requested
    role_filter = request.GET.get('role')
    tenant_filter = request.GET.get('tenant')

    if role_filter:
        audits = audits.filter(user__role=role_filter)
    if tenant_filter:
        audits = audits.filter(tenant_id=tenant_filter)

    roles = CustomUser.objects.values_list('role', flat=True).distinct()
    tenants = Tenant.objects.all()

    return render(request, 'audit/audit_list.html', {
        'audits': audits,
        'roles': roles,
        'tenants': tenants
    })

# View monitoring logs (accessible only by superadmin)
@user_passes_test(is_superadmin)
def monitoring_list(request):
    monitorings = Monitoring.objects.all()

    # Filtering by role and tenant if requested
    role_filter = request.GET.get('role')
    tenant_filter = request.GET.get('tenant')

    if role_filter:
        monitorings = monitorings.filter(user__role=role_filter)
    if tenant_filter:
        monitorings = monitorings.filter(tenant_id=tenant_filter)

    roles = CustomUser.objects.values_list('role', flat=True).distinct()
    tenants = Tenant.objects.all()

    return render(request, 'audit/monitoring_list.html', {
        'monitorings': monitorings,
        'roles': roles,
        'tenants': tenants
    })
