from django.urls import path
from . import views

urlpatterns = [
    # Liste des taux pour les membres
    path('list/', views.taux_list, name='taux-list'),
    
    # Création d'un taux pour les membres
    path('create/', views.create_taux, name='create-taux'),
    
    # Mise à jour d'un taux pour les membres
    path('update/<int:taux_id>/', views.update_taux, name='update-taux'),
    
    # Suppression d'un taux pour les membres
    path('delete/<int:taux_id>/', views.delete_taux, name='delete-taux'),

    # Superadmin voit les taux d'un tenant
    path('view/<int:tenant_id>/', views.view_taux_tenant, name='view-taux-tenant'),
]
