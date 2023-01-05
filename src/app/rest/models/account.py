from app.rest.utils import AXESS
from django.db import models
from uuid import uuid4


class Account(models.Model):
    name = models.CharField(verbose_name='Name', max_length=32)
    active = models.BooleanField(verbose_name='Active', default=True)

    rest_url = models.URLField(verbose_name='REST URL')
    login_id = models.CharField(verbose_name='Login ID', max_length=32)
    username = models.CharField(verbose_name='Username', max_length=32)
    password = models.CharField(verbose_name='Password', max_length=32)
    soap_username = models.CharField(verbose_name='Username', max_length=32)
    soap_password = models.CharField(verbose_name='Password', max_length=32)

    access_token = models.UUIDField(
        verbose_name='Access Token', primary_key=True, default=uuid4)

    last_request = models.DateTimeField(verbose_name='Last Request', null=True)

    def __str__(self):
        return self.name

    @property
    def session(self):
        return self.session_set.filter(
            active=True,
        ).first()

    def new_session(self):
        session_id = AXESS(self).create_session()

        if session_id:
            return self.session_set.create(
                session_id=session_id,
                account=self,
            )

        return None
