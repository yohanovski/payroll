from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.paie_list, name='paie-list'),
    path('create/', views.create_paie, name='create-paie'),
    path('detail/<int:paie_id>/', views.detail_paie, name='detail-paie'),
    path('edit/<int:paie_id>/', views.edit_paie, name='edit-paie'),
    path('delete/<int:paie_id>/', views.delete_paie, name='delete-paie'),
]
