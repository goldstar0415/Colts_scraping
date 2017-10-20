import uuid
from django.db import models
from django.contrib.auth.models import User


class HashTag(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    tag = models.CharField(max_length=40, null=True, blank=True, verbose_name='Tag')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hashtag')
    networks = models.ManyToManyField('social_parsing.Network', blank=True, verbose_name='Social network', through='hashtag_network.HashTagNetwork', related_name='hashtags')
    is_active = models.NullBooleanField(null=True, blank=True, verbose_name='Active')

    class Meta:
        verbose_name = "Hashtag"
        verbose_name_plural = "Hashtags"

    def __str__(self):
        return '{}'.format(self.tag)
