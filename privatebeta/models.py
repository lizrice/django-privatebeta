import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

import logging
log = logging.getLogger("movieminder")

class InviteRequest(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    created = models.DateTimeField(_('Created'), default=datetime.datetime.now)
    invited = models.BooleanField(_('Invited'), default=False)

    def __unicode__(self):
        return _('Invite for %(email)s') % {'email': self.email}

    def _get_accepted(self):
        match = User.objects.filter(email__iexact=self.email)
        return match.exists()
    
    accepted = property(_get_accepted)
    