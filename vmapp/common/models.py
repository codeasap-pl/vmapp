from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    ctime = models.DateTimeField(null=False, blank=True, auto_now_add=True)
    mtime = models.DateTimeField(null=False, blank=True, auto_now=True)
