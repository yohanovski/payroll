from django import forms
from .models import Tenant, TenantInfo

class TenantCreationForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'on_trial', 'limit_date', 'description', 'active']

class TenantInfoForm(forms.ModelForm):
    class Meta:
        model = TenantInfo
        fields = ['raison_social', 'type', 'RC', 'IF', 'patente', 'CNSS', 'ICE']
