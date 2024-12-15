from django.contrib import admin

from checkout.models import Order
from django.http import HttpResponse
import csv


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "total_amount",
        "course",
        "course__id",
        "status_display",
        "created_at",
        "updated_at",
    )
    search_fields = ("buyer__username", "course__name", "status", "course__id")
    list_filter = ("created_at", "updated_at", "status", "buyer__name")
    actions = ["export_as_csv"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=...):
        return False

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

    def status_display(self, obj):
        return "Paid" if obj.status == 1 else "Pending"

    status_display.short_description = "Status"


admin.site.register(Order, OrderAdmin)
