from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from tenant.models import Tenant

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, tenant=None, role='member', **extra_fields):
        """
        Create and return a regular user with an email, role, and tenant.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the role of 'superadmin'.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')  # Set default role to 'superadmin'

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)  # No need to pass role explicitly

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
        ('superadmin', 'Superadmin'),
    )

    username = None  # Remove the username field
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Provide a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Provide a unique related_name
        blank=True
    )

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No other required fields

    objects = CustomUserManager()  # Use the custom manager

    def save(self, *args, **kwargs):
        if self.role == 'superadmin':
            self.tenant = None  # Ensure that superadmin has no tenant
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
