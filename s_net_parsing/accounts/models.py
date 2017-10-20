import uuid
from django.db import models


class Account(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    token = models.CharField(max_length=400, null=True, blank=True, verbose_name='Network token')
    login = models.CharField(max_length=100, null=True, blank=True, verbose_name='Network login')
    password = models.CharField(max_length=100, null=True, blank=True, verbose_name='Network password')
    network = models.ForeignKey('social_parsing.Network', null=True, blank=True, verbose_name='Social network')
    refresh_time = models.DateTimeField(null=True, blank=True, verbose_name="When limit will be renewed")
    is_limited = models.BooleanField(verbose_name='Queries limit')
    is_active = models.BooleanField(verbose_name='Active/Blocked')

    class Meta:
        verbose_name = "Social network account"
        verbose_name_plural = "Social network accounts"

    def __str__(self):
        return '{} {}'.format(self.network, self.login)
