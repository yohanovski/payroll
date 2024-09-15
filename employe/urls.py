# employe/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_employe, name='create-employe'),
    path('update/<int:employe_id>/', views.update_employe, name='update-employe'),
    path('delete/<int:employe_id>/', views.delete_employe, name='delete-employe'),
    path('list/', views.employe_list, name='employe-list'),
    path('detail/<int:employe_id>/', views.employe_detail, name='employe-detail'),
    path('create-enfant/<int:employe_id>/', views.create_enfant, name='create-enfant'),
    path('update-enfant/<int:enfant_id>/', views.update_enfant, name='update-enfant'),
    path('delete-enfant/<int:enfant_id>/', views.delete_enfant, name='delete-enfant'),
    path('enfant-detail/<int:enfant_id>/', views.enfant_detail, name='enfant-detail'),
]
