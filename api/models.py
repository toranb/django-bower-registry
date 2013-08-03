from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=500, db_index=True, unique=True)
    url = models.CharField(max_length=500, unique=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta(object):
        unique_together = ('name', 'url')
