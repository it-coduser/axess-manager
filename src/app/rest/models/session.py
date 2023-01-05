from app.rest.models import AccountModel
from app.rest.utils import AXESS
from django.db import models


class Session(models.Model):
    account = models.ForeignKey(
        verbose_name='Account', to=AccountModel, on_delete=models.CASCADE)

    active = models.BooleanField(verbose_name='Active', default=True)

    session_id = models.BigIntegerField(
        verbose_name='Session ID', unique=True, editable=False)

    created_at = models.DateTimeField(
        verbose_name='Created At', auto_now_add=True)

    def __str__(self):
        return str(self.session_id)

    def save(self, *args, **kwargs):
        sessions = Session.objects.filter(
            active=True,
            account=self.account
        )

        for session in sessions:
            session.delete()

        sessions.update(active=False)

        super(Session, self).save(*args, **kwargs)

    def is_valid(self):
        return AXESS(self.account).check_session(self)

    def delete(self, using=None, keep_parents=False):
        return AXESS(self.account).delete_session(self)
