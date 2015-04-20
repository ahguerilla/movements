import logging

from django.core.management.base import BaseCommand

from app.market.models import Comment, MarketItem
from app.market.models.translation import detect_language

_logger = logging.getLogger('movements-alerts')


class Command(BaseCommand):
    args = ''
    help = 'Attempts to detect the langauge for all posts and comments through google.'

    def handle(self, *args, **options):
        _logger.debug('Starting language auto-detection')
        for item in MarketItem.objects.all():
            try:
                item.language = detect_language(item.details)
                item.save(update_fields=['language'])
            except Exception as ex:
                _logger.exception(ex)
        for comment in Comment.objects.all():
            try:
                comment.language = detect_language(comment.contents)
                comment.save(update_fields=['language'])
            except Exception as ex:
                _logger.exception(ex)


