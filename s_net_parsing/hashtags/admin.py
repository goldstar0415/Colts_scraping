from django.contrib import admin
from hashtags.models import HashTag


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    model = HashTag
    list_display = ("tag", "user")
    list_filter = ("tag", "user")
