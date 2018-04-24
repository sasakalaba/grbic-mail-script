from django.db import models


class Directory(models.Model):
    title = models.CharField(max_length=100)
    dir_id = models.CharField(max_length=50)
    urls_id = models.CharField(max_length=50, blank=True, null=True)
    emails_id = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Directories"

    def __str__(self):
        return self.title
