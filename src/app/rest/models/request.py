from app.rest.models import SessionModel
from django.utils import timezone
from django.db import models


class Request(models.Model):
    session = models.ForeignKey(
        verbose_name='Session', to=SessionModel, on_delete=models.CASCADE)

    ip_address = models.GenericIPAddressField(verbose_name='IP Address')
    response = models.JSONField(verbose_name='Response', editable=False)
    payload = models.JSONField(verbose_name='Request', editable=False)
    method = models.CharField(verbose_name='Method', max_length=32)

    created_at = models.DateTimeField(
        verbose_name='Created At', auto_now_add=True)

    def __str__(self):
        return self.method

    def save(self, *args, **kwargs):
        account = self.session.account
        account.last_request = timezone.now()
        account.save()

        super(Request, self).save(*args, **kwargs)
