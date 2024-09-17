from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import UserCreationForm
from .models import CustomUser
from tenant.models import Tenant
from audit.models import Audit, Monitoring  # Import des modèles d'audit et monitoring
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

# Custom Login View with Role-Based Redirection
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('tenant-list')  # Superuser to tenant list
        elif user.role == 'admin' or user.role == 'member':
            return reverse_lazy('employe-list')  # Admin/Member to employee list
        return reverse_lazy('home')  # Default redirect

# Superuser creates users
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Enregistrer l'action dans l'audit
            Audit.objects.create(
                user=request.user,
                tenant=user.tenant,
                table_name='CustomUser',
                row_id=user.id,
                column_name='All',
                old_value='',
                new_value=str(user),
                change_date=timezone.now()
            )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=user.tenant,
                activity='User Created',
                description=f'User {user.email} was created',
                timestamp=timezone.now()
            )
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

    # Enregistrer dans le monitoring
    Monitoring.objects.create(
        user=request.user,
        tenant=None,  # Pas nécessaire pour cette action spécifique
        activity='User List Viewed',
        description='Superadmin viewed the user list',
        timestamp=timezone.now()
    )

    return render(request, 'users/user_list.html', {'users': users, 'tenants': tenants})

# Edit a user
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    old_user_data = user.__dict__.copy()  # Sauvegarder l'état avant la mise à jour

    if request.method == 'POST':
        form = UserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Comparer les anciennes et nouvelles données pour l'audit
            for field in form.changed_data:
                old_value = old_user_data[field]
                new_value = getattr(user, field)
                Audit.objects.create(
                    user=request.user,
                    tenant=user.tenant,
                    table_name='CustomUser',
                    row_id=user.id,
                    column_name=field,
                    old_value=str(old_value),
                    new_value=str(new_value),
                    change_date=timezone.now()
                )
            # Enregistrer dans le monitoring
            Monitoring.objects.create(
                user=request.user,
                tenant=user.tenant,
                activity='User Updated',
                description=f'User {user.email} was updated',
                timestamp=timezone.now()
            )
            return redirect('user-list')
    else:
        form = UserCreationForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form})

# Delete a user
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        # Enregistrer l'action dans l'audit avant la suppression
        Audit.objects.create(
            user=request.user,
            tenant=user.tenant,
            table_name='CustomUser',
            row_id=user.id,
            column_name='All',
            old_value=str(user),
            new_value='Deleted',
            change_date=timezone.now()
        )
        user.delete()
        # Enregistrer dans le monitoring
        Monitoring.objects.create(
            user=request.user,
            tenant=user.tenant,
            activity='User Deleted',
            description=f'User {user.email} was deleted',
            timestamp=timezone.now()
        )
        return redirect('user-list')
    return render(request, 'users/confirm_delete.html', {'user': user})
