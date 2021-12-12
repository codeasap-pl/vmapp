from django.db import models
from common.models import BaseModel


class Alias(BaseModel):
    class Meta:
        db_table = "aliases"
        verbose_name_plural = "aliases"
        unique_together = [
            ["email", "alias"]
        ]

    email = models.EmailField(null=False, max_length=255)
    alias = models.EmailField(null=False, max_length=255)
    is_enabled = models.BooleanField(default=True)
