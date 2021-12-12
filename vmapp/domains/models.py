from django.db import models
from common.models import BaseModel


class Domain(BaseModel):
    class Meta:
        db_table = "domains"

    domain = models.CharField(null=False, unique=True,
                              max_length=255)  # RFC1035
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.domain
