from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from app.users.models import UserProfile
from app.market.models import MarketItem
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    args = ''
    help = 'Assign users to groups based on skills and site actions'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for u in all_users:
            try:
                profile = UserProfile.objects.get(user=u)
            except ObjectDoesNotExist:
                profile = None
            if not profile:
                continue
            has_request = MarketItem.objects.filter(owner=u, item_type='request').count() > 0
            has_offer = MarketItem.objects.filter(owner=u, item_type='offer').count() > 0
            profile.assign_group_based_on_skills(has_offer, has_request)
