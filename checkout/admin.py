from django.contrib import admin

from checkout.models import Order


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "total_amount",
        "status",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__username", "course__name")
    list_filter = ("created_at", "updated_at", "status", "user__name")


admin.site.register(Order, OrderAdmin)
