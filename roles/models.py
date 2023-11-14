from django.db import models
from django.core.exceptions import ValidationError

from branches.models import Branches


class Roles(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        db_table = "roles"
        app_label = "roles"

    def __repr__(self) -> str:
        return f"<Role {self.id} - {self.name}>"

    def __str__(self):
        return f"<Role {self.id} - {self.name}>"
