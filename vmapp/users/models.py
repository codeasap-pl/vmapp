import crypt
from django.db import models
from common.models import BaseModel
from domains.models import Domain


class User(BaseModel):
    class Meta:
        db_table = "users"
        unique_together = [
            ["username", "domain"]
        ]

    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    username = models.CharField(null=False, max_length=64)
    password = models.CharField(null=False, max_length=256)
    quota = models.PositiveIntegerField(default=134217728)
    is_enabled = models.BooleanField(default=True)

    @classmethod
    def from_db(cls, db, field_names, values):
        obj = super().from_db(db, field_names, values)
        obj.quota = obj.quota / 1024 / 1024
        return obj

    def save(self, *args, **kwargs):
        # QUOTA: megabytes to bytes
        self.quota = self.quota * 1024 * 1024

        # HASH password
        algo = "{SHA512-CRYPT}"
        if not self.password.startswith("%s$6$" % algo):
            salt = crypt.mksalt(method=crypt.METHOD_SHA512)
            self.password = "{algo}{crypted}".format(
                algo=algo,
                crypted=crypt.crypt(self.password, salt)
            )
        super().save(*args, **kwargs)

    def email(self):
        return "%s@%s" % (self.username, self.domain.domain)

    def __str__(self):
        return self.email()
