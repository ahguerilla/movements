from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^open-graph$', 'app.market.test.views.open_graph', name="open_graph"),
)
