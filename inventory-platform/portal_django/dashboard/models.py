from django.db import models


class BranchDirectory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=255)
    timezone = models.CharField(max_length=64, default='UTC')

    def __str__(self):
        return self.name
