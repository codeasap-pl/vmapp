from django.contrib import admin
from django.db.models import Q, Count
from .models import Domain


@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = (
        "domain", "is_enabled", "total_users", "total_active_users",
        "ctime", "mtime"
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            total_users=Count(
                "user",
            ),
            total_active_users=Count(
                "user",
                filter=Q(user__is_enabled=True)
            )

        )
        return qs

    def total_users(self, obj):
        return obj.total_users

    def total_active_users(self, obj):
        return obj.total_active_users
