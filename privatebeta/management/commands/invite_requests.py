from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from privatebeta.models import InviteRequest
from datetime import datetime, timedelta


class Command(BaseCommand):
    args = 'invitation code'
    help = 'Output something to paste into Mailchimp'

    def handle(self, *args, **options):
        try:
            code = args[0]
        except:
            print "You need to supply an invitation code"  
            return
              
        invitees = InviteRequest.objects.filter(invited=False)
        last_week = datetime.now() - timedelta(days=7)     
        invitees = invitees.filter(created__gte=last_week)
        
        for ir in invitees:
            print "{0}, {1}".format(ir.email, code)