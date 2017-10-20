from django.contrib import admin
from accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ("login", "related_network", "is_active", )
    list_filter = ("is_active",)
    search_fields = ("login", )

    def related_network(self, obj):
        return '{}'.format(obj.network)
    related_network.short_description = 'Social network'
