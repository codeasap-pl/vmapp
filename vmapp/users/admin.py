from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email", "username", "domain", "is_enabled", "quota",
        "ctime", "mtime", "is_domain_enabled",
    )

    def is_domain_enabled(self, obj):
        return obj.domain.is_enabled
