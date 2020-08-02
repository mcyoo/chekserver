from django.db import models
from core import models as core_models


class User(core_models.TimeStampedModel):

    ANDROID = "android"
    APPLE = "ios"
    OTHER = "other"

    PHONE_CHOICES = ((ANDROID, "Android"), (APPLE, "ios"), (OTHER, "Other"))

    token = models.CharField(max_length=300)
    user_os = models.CharField(choices=PHONE_CHOICES, max_length=10, blank=True)
    user_ver = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.token
