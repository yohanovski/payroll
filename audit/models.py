from django.db import models
from tenant.models import Tenant
from users.models import CustomUser  # Corrected import for the CustomUser model

class Audit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,null=True,blank=True)
    table_name = models.CharField(max_length=50)
    row_id = models.CharField(max_length=50)  # Allows for more flexibility (e.g., UUID)
    column_name = models.CharField(max_length=50)
    old_value = models.TextField()
    new_value = models.TextField()
    change_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-change_date']

    def __str__(self):
        return f'Change in {self.table_name} by {self.user} on {self.change_date}'

class Monitoring(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use CustomUser
    activity = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.activity} for {self.tenant} at {self.timestamp}'
