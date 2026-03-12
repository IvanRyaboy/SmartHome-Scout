import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Role(models.Model):
    """Role for access levels: guest, user, moderator, administrator."""
    NAME_GUEST = 'guest'
    NAME_USER = 'user'
    NAME_MODERATOR = 'moderator'
    NAME_ADMINISTRATOR = 'administrator'
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'accounts_role'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )

    def get_absolute_url(self):
        return reverse('accounts:profile', args=[str(self.id)])

    @property
    def is_administrator_role(self):
        return self.role and self.role.name == Role.NAME_ADMINISTRATOR

    @property
    def is_moderator_role(self):
        return self.role and self.role.name == Role.NAME_MODERATOR


class AuditLog(models.Model):
    """Journal of data changes for auditing."""
    class Action(models.TextChoices):
        INSERT = 'insert', 'Insert'
        UPDATE = 'update', 'Update'
        DELETE = 'delete', 'Delete'

    id = models.BigAutoField(primary_key=True)
    user_id = models.UUIDField(null=True, blank=True, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    table_name = models.CharField(max_length=128)
    record_id = models.CharField(max_length=64, blank=True)
    action = models.CharField(max_length=10, choices=Action.choices)
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'accounts_auditlog'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} {self.table_name}.{self.record_id} at {self.timestamp}"
