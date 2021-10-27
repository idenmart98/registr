from django.db import models
from django.contrib.auth.models import User

from django.utils.crypto import get_random_string

class ConfirmationCode(models.Model):
    user = models.ForeignKey(User, related_name='codes', on_delete=models.CASCADE)
    code = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=8)

        super(ConfirmationCode, self).save(*args, **kwargs)

