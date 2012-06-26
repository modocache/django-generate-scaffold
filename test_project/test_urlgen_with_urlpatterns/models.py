from django.db import models
from django.utils.timezone import now


class URLPreExistingDatedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, default=now(), editable=False)
