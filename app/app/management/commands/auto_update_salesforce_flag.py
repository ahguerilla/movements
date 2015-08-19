from django.core.management.base import BaseCommand
from app.market.models import MarketItem, MarketItemSalesforceRecord
import logging
logger = logging.getLogger('notifications')


class Command(BaseCommand):
    args = ''
    help = 'set salesforce records to update'

    def handle(self, *args, **options):
        market_items = MarketItem.objects.exclude(staff_owner__isnull=True).all()
        for m in market_items:
            try:
                MarketItemSalesforceRecord.mark_for_update(m.id)
            except Exception as ex:
                logger.exception(ex.message)