import uuid

from django.db import models


class BaseModel(models.Model):
    """Basic Model"""

    date_added = models.DateTimeField(auto_now=True)
    date_changed = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True
        ordering = ("-date_added",)