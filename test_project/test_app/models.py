from django.db import models
from django.utils.timezone import now


class PreExistingModel(models.Model):
    description = models.TextField()


class PreExistingDatedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, default=now(), editable=False)
