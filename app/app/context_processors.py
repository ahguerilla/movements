from django.utils.translation import ugettext as _
from django.conf import settings
import json


def app_settings(context):
    return {
        'settings': {
            'ADMIN_ENABLED': settings.ADMIN_ENABLED,
        }
    }


def string_constants(context):
    constants = json.dumps(
        {
            'exchange': _('Exchange'),
            'members': _('Members'),
            'recommendation': _('Recommendation'),
            'more': _('more...'),
            'view_recommendation': _('Click here to view the recommendation'),
            'offering': _('Offering'),
            'requesting': _('Requesting'),
            'user_search_by_params': _('Search by keyword or username for Members'),
            'market_search_no_match_a': _('Your search did not match any market item.'),
            'market_search_no_match_b': _('Search again without any filters'),
            'market_search_no_match_c': _('or'),
            'market_search_no_match_d': _('search again with your default filters'),
            'redirect_off_site': _('This link will take you off the Movements site.\nMake sure you trust the site that you are being redirected to.'),
            'signup_text': _('SIGNUP'),
            'signup_login_text': _('LOGIN OR SIGNUP'),
        })

    return {
        'string_constants': constants
    }
