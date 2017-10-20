from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from .imglib import resize_image


class SimpleUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="users_avatar/", verbose_name='Users image', null=True, blank=True, )
    bio = models.TextField(max_length=400, null=True, blank=True, verbose_name='Short bio')
    country_name = CountryField(blank_label='(choose country)', null=True, blank=True, verbose_name='Country of origin')
    company = models.CharField(max_length=50, null=True, blank=True, verbose_name='Company name')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Birth date')

    def save(self, *args, **kwargs):
        super(SimpleUsers, self).save(*args, **kwargs)
        if self.avatar:
            resize_image(self.avatar)

    def __unicode__(self):
        return self.user.username
