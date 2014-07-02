from __future__ import absolute_import

import logging

from django.core.management.base import BaseCommand

import time

logger = logging.getLogger('notifications')


class Command(BaseCommand):
    args = ''
    help = 'Runs the movements notifications process'

    def handle(self, *args, **options):
        while True:
            logger.info('Running the notification process')
            try:
                pass
            except Exception as ex:
                logger.exception(ex)
            time.sleep(1)
