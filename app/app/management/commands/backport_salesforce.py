from __future__ import absolute_import
from django.core.management.base import BaseCommand
from app.sforce import run_backport


class Command(BaseCommand):
    """
    Django management command to sanitise a database of any live user info.
    """
    args = ''
    help = "Creates salesforce records for cases that don't exist"

    def handle(self, *args, **options):
        try:
            run_backport()
        except Exception as ex:
            print "Failed to run backport of salesforce records"
