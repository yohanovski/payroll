from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_tenant, name='create-tenant'),
    path('create-info/<int:tenant_id>/', views.create_tenant_info, name='create-tenant-info'),
    path('update-info/<int:tenant_id>/', views.update_tenant_info, name='update-tenant-info'),
    path('info/<int:tenant_id>/', views.view_tenant_info, name='view-tenant-info'),  # Accept tenant_id as argument
    path('list/', views.tenant_list, name='tenant-list'),
    path('update/<int:tenant_id>/', views.update_tenant, name='update-tenant'),
    path('delete/<int:tenant_id>/', views.delete_tenant, name='delete-tenant'),
]
