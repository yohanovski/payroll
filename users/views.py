from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import UserCreationForm
from .models import CustomUser
from tenant.models import Tenant

# Superuser creates users
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = UserCreationForm()
    return render(request, 'users/create_user.html', {'form': form})

# List users and filter by role and tenant (for superusers only)
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    role_filter = request.GET.get('role', None)
    tenant_filter = request.GET.get('tenant', None)

    users = CustomUser.objects.all()

    if role_filter:
        users = users.filter(role=role_filter)
    if tenant_filter:
        users = users.filter(tenant_id=tenant_filter)

    tenants = Tenant.objects.all()

    return render(request, 'users/user_list.html', {'users': users, 'tenants': tenants})

# Edit a user
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = UserCreationForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form})

# Delete a user
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('user-list')
