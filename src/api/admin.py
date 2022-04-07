from django.contrib import admin
from .models import Bond


class BondAdmin(admin.ModelAdmin):
    list_display = (
        "bond_type",
        "no_of_bonds",
        "selling_price",
        "seller",
        "status",
        "buyer",
        "price_in_usd",
        "created_at",
    )


admin.site.register(Bond, BondAdmin)

admin.site.site_header = "Trading App"
