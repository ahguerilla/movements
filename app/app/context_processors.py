from django.utils.translation import ugettext as _
import json

def string_constants(context):
    string_constants = json.dumps(
        {
            'exchange': _('Exchange'),
            'members': _('Members'),
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
        })

    return {
        'string_constants': string_constants 
    }