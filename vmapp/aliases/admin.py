from django.contrib import admin
from .models import Alias


@admin.register(Alias)
class AliasAdmin(admin.ModelAdmin):
    list_display = ("email", "alias", "is_enabled", "ctime", "mtime")

    def email(self, obj):
        return "%s@%s" % (obj.username, obj.domain.domain)
