from django.db import models

# Create your models here.
from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    on_trial = models.BooleanField(default=False)
    limit_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Tenant"
        verbose_name_plural = "Tenants"

class TenantInfo(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    raison_social = models.CharField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    RC = models.CharField(max_length=50, null=True, blank=True)
    IF = models.CharField(max_length=50, null=True, blank=True)
    patente = models.CharField(max_length=50, null=True, blank=True)
    CNSS = models.CharField(max_length=50, null=True, blank=True)
    ICE = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Info for {self.tenant.name}"