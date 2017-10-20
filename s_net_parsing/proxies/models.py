import uuid
from django.db import models


class Proxy(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    url = models.CharField(max_length=200, null=True, blank=True, verbose_name='Proxy URL')
    expires = models.DateTimeField(verbose_name='Pay expiration date and time')
    is_active = models.BooleanField(verbose_name='Active')
    is_banned = models.BooleanField(verbose_name='Blacklisted')

    class Meta:
        verbose_name = "Proxy address"
        verbose_name_plural = "Proxy addresses"

    def __str__(self):
        return '{}'.format(self.url)
