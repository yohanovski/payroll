from django.urls import path
from . import views

urlpatterns = [
    path('audits/', views.audit_list, name='audit-list'),
    path('monitorings/', views.monitoring_list, name='monitoring-list'),
]
