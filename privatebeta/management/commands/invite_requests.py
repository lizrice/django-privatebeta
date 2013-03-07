from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from privatebeta.models import InviteRequest
from datetime import datetime, timedelta
from optparse import make_option

class Command(BaseCommand):
    args = 'invitation code'
    help = 'Output something to paste into Mailchimp'
    option_list = BaseCommand.option_list + (
        make_option('--update',
            action='store_true',
            dest='update',
            default=False,
            help='Mark the invitees as invited'),
        )


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
            if options['update']:
                ir.invited = True
                ir.save()
        