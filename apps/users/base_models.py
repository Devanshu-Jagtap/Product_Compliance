from django.db import models

class BaseContent(models.Model):
    createdDate = models.DateTimeField(auto_now_add=True)
    lastUpdatedDate = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True