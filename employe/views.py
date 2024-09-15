# employe/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import EmployeForm, EnfantForm
from .models import Employe, Enfants
from tenant.models import Tenant

# Check if user is admin or member
def is_admin_or_member(user):
    return user.role in ['admin', 'member']

# List employees (accessible by admin or member)
@user_passes_test(is_admin_or_member)
def employe_list(request):
    employes = Employe.objects.filter(tenant=request.user.tenant)  # Filter employees by tenant
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
            return redirect('employe-list')
    else:
        form = EmployeForm()
    return render(request, 'employe/create_employe.html', {'form': form})

# Update an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def update_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect('employe-list')
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'employe/update_employe.html', {'form': form})

# Delete an employee (only admin or member)
@user_passes_test(is_admin_or_member)
def delete_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    employe.delete()
    return redirect('employe-list')

# View employee details
@user_passes_test(is_admin_or_member)
def employe_detail(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id, tenant=request.user.tenant)
    enfants = Enfants.objects.filter(employe=employe)
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
            return redirect('employe-detail', employe_id=employe.id)
    else:
        form = EnfantForm()
    return render(request, 'employe/create_enfant.html', {'form': form, 'employe': employe})

# Update an enfant (only admin or member)
@user_passes_test(is_admin_or_member)
def update_enfant(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    if request.method == 'POST':
        form = EnfantForm(request.POST, instance=enfant)
        if form.is_valid():
            form.save()
            return redirect('employe-detail', employe_id=enfant.employe.id)
    else:
        form = EnfantForm(instance=enfant)
    return render(request, 'employe/update_enfant.html', {'form': form})

# Delete an enfant (only admin or member)
@user_passes_test(is_admin_or_member)
def delete_enfant(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    enfant.delete()
    return redirect('employe-detail', employe_id=enfant.employe.id)

# View enfant details
@user_passes_test(is_admin_or_member)
def enfant_detail(request, enfant_id):
    enfant = get_object_or_404(Enfants, id=enfant_id, employe__tenant=request.user.tenant)
    return render(request, 'employe/enfant_detail.html', {'enfant': enfant})
