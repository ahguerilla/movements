from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from app.users.models import UserProfile, Countries, Region
from app.market.models import MarketItem
from django.core.exceptions import ObjectDoesNotExist
import logging
import csv

logger = logging.getLogger('notifications')


class Command(BaseCommand):
    args = ''
    help = 'User analytics 0620'

    def handle(self, *args, **options):
        user_list = []
        all_users = User.objects.all()[:50]

        middle_east_region = Region.objects.get(name='Middle East')
        count_all = Countries.objects.all().count()
        count_middle_east = Countries.objects.filter(region=middle_east_region).count()

        journalist_group = Group.objects.get(name='Journalist')
        lawyer_group = Group.objects.get(name='Lawyers')
        provider_group = Group.objects.get(name='Provider')

        for u in all_users:
            try:
                profile = UserProfile.objects.get(user=u)
            except ObjectDoesNotExist:
                profile = None
            if not profile:
                continue

            u_countries = profile.countries.all()
            u_countries_name = [c.countries for c in u_countries]
            if 'Iran' in u_countries_name:
                has_iran = True
            else:
                has_iran = False

            if u_countries.count() == count_all:
                has_all_countries = True
            else:
                has_all_countries = False

            if u_countries.filter(region=middle_east_region).count() == count_middle_east:
                has_all_middle_east = True
            else:
                has_all_middle_east = False

            has_request = MarketItem.objects.filter(owner=u, item_type='request').count() > 0
            has_offer = MarketItem.objects.filter(owner=u, item_type='offer').count() > 0

            if journalist_group in u.groups.all():
                in_journalist_group = True
            else:
                in_journalist_group = False

            if lawyer_group in u.groups.all():
                in_lawyer_group = True
            else:
                in_lawyer_group = False

            if provider_group in u.groups.all():
                in_provider_group = True
            else:
                in_provider_group = False

            u_skills = profile.skills.all()
            u_skills_list = " ".join([s.skills for s in u_skills])

            user = {
                'id': u.id,
                'email': u.email,
                'username': u.username,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'has_iran': has_iran,
                'has_all_middle_east': has_all_middle_east,
                'has_all_countries': has_all_countries,
                'has_request': has_request,
                'has_offer': has_offer,
                'in_journalist_group': in_journalist_group,
                'in_lawyer_group': in_lawyer_group,
                'in_provider_group': in_provider_group,
                'skills_list': u_skills_list
            }

            user_list.append(user)

        with open('user_list.csv', 'wb') as write_file:
            w = csv.writer(write_file)
            w.writerow(['ID', 'EMAIL', 'USERNAME', 'IRAN SELECTED', 'MIDDLE EAST SELECTED', 'ALL COUNTRIES SELECTED',
                        'HAS POSTED OFFER', 'HAS POSTED REQUEST', 'MEMBER OF PROVIDERS', 'MEMBER OF LAWYERS',
                        'MEMBER OF JOURNALIST GROUP', 'SKILLS'])
            for u in user_list:
                row = [u['id'], u['email'], u['username'], u['has_iran'], u['has_all_middle_east'],
                       u['has_all_countries'], u['has_offer'], u['has_request'], u['in_provider_group'],
                       u['in_lawyer_group'], u['in_journalist_group'], u['skills_list']]
                w.writerow(row)
