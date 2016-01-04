from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from app.market.models import MarketNewsItemData

import json


@require_POST
@login_required
def parse_url(request):
    url = request.POST.get('url')
    if not request.is_ajax() or not url:
        return HttpResponseBadRequest()
    try:
        article = MarketNewsItemData.fetch_news_item(url)
    except ValueError:
        return HttpResponse(json.dumps({'success': False}), mimetype="application/json")
    data = article.format_for_news_card()
    data.update({'success': True})
    return HttpResponse(json.dumps(data), mimetype="application/json")