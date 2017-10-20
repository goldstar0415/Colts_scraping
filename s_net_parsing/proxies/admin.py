from django.contrib import admin
from proxies.models import Proxy


@admin.register(Proxy)
class ProxyAdmin(admin.ModelAdmin):
    model = Proxy
    list_display = ("url", "expires", "is_active", "is_banned", )
    list_filter = ("url", "expires", "is_active", "is_banned", )
