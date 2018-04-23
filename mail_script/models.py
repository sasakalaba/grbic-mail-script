from django.db import models


class Directory(models.Model):
    title = models.CharField(max_length=100)
    dir_id = models.CharField(max_length=50)
    url = models.URLField(max_length=300)

    class Meta:
        verbose_name_plural = "Directories"
