from __future__ import absolute_import
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    """
    Django management command to sanitise a database of any live user info.
    """
    args = ''
    help = 'Runs the movemetns sanitisater'

    user_whitelist = {'aidan.hamade@gmail.com', 'aidan@guerillasoftware.net'}
    domain_whitelist = {}

    def handle(self, *args, **options):
        anon_count = 1
        try:
            for user in User.objects.all():
                if user.email in self.user_whitelist:
                    continue
                split_email = user.email.rsplit('@', 1)
                if len(split_email) == 2 and split_email[1] in self.domain_whitelist:
                    continue
                user.email = 'anon{0}@movements.org'.format(anon_count)
                user.first_name = 'Anon'
                user.last_name = str(anon_count)
                user.set_password('password')
                user.save(update_fields=["password", "email", "first_name", "last_name"])
                anon_count += 1
        except Exception as ex:
            print "Failed to Sanitise Database"
