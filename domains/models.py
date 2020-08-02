from django.db import models
from core import models as core_models


class Domain(core_models.TimeStampedModel):

    url = models.CharField(max_length=300)
    token = models.ForeignKey(
        "users.User", related_name="domains", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100, default="", blank=True)
    html = models.CharField(max_length=50, default="", blank=True)
    change = models.BooleanField(default=False)

    def __str__(self):
        return self.url
