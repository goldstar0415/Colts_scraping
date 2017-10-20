import uuid
from django.db import models
from django.core.exceptions import ValidationError


class Network(models.Model):
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit * 640 * 640:
            raise ValidationError("File is too big.")

    guid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='Name')
    icon_pic = models.FileField(upload_to="network_pic/", verbose_name='Social network icon',
                                null=True, blank=True, validators=[validate_image])
    parsing_frequency = models.PositiveIntegerField(default=60,
                                                    blank=True,
                                                    null=True,
                                                    verbose_name='The number of seconds between parsing attempts.')

    class Meta:
        verbose_name = "Name of the social network"
        verbose_name_plural = "Networks name"

    def __str__(self):
        return '{}'.format(self.name)
