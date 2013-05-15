from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from privatebeta.models import InviteRequest
from datetime import datetime, timedelta
from optparse import make_option
import mailchimp.utils
from django.conf import settings

class Command(BaseCommand):
    args = 'invitation code'
    help = 'Invite the users who have not been invited yet'
    option_list = BaseCommand.option_list + (
        make_option('--update',
            action='store_true',
            dest='update',
            default=False,
            help='Mark the invitees as invited in the database'),
        make_option('--mailchimp',
            action='store_true',
            dest='mailchimp',
            default=False,
            help='Update Mailchimp with the invitation code'),
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

        if options['mailchimp']:

            if not getattr(settings, "MAILCHIMP_SUBSCRIBE", False):
                print "MAILCHIMP_SUBSCRIBE is not set"
                return

            mc_invite_request_list = mailchimp.utils.get_connection().get_list_by_id(settings.MAILCHIMP_INVITATION_REQUEST_LIST_ID)
        else:
            mc_invite_request_list = None

        for ir in invitees:
            print "{0}, {1}".format(ir.email, code)
            if options['mailchimp']:
                try:
                    mc_invite_request_list.subscribe(ir.email, {'INVITATION': code, 'SEND_INV': 'Go'}, double_optin=False, update_existing=True)
                except Exception, e:
                    print "Problem subscribing {0} to Mailchimp list {1}".format(ir.email)

            if options['update']:
                ir.invited = True
                ir.save()
