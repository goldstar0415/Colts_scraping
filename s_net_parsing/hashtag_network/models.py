from django.db import models


class HashTagNetwork(models.Model):
    hashtag = models.ForeignKey('hashtags.HashTag', on_delete=models.CASCADE)
    network = models.ForeignKey('social_parsing.Network', on_delete=models.CASCADE)
    last_scraped = models.DateTimeField(null=True, blank=True, verbose_name='Last parsing date and time')
