from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _
from app.market.models import MarketNewsItemData

import json


@require_POST
def parse_url(request):
    url = request.POST.get('url')
    if not request.is_ajax() or not url:
        return HttpResponseBadRequest()
    try:
        article = MarketNewsItemData.fetch_news_item(url)
    except ValueError:
        return HttpResponse(json.dumps({'success': False, 'message': _('Unable to parse url')}))

    data = {
        'success': True,
        'title': article.title,
        'description': article.description,
        'site_name': article.site_name,
        'image': article.image,
        'author': article.author_name
    }

    return HttpResponse(json.dumps(data))