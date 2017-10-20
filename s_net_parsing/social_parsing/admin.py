from django.contrib import admin
from social_parsing.models import Network


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    model = Network
    list_display = ("name", "parsing_frequency", )
    list_filter = ("name", "parsing_frequency", )
    search_fields = ('name',)
