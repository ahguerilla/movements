from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^open-graph$', 'app.market.test.views.open_graph', name="open_graph"),
    url(r'^open-graph-author$', 'app.market.test.views.open_graph_author', name="open_graph_author"),
    url(r'^open-graph-date1$', 'app.market.test.views.open_graph_date1', name="open_graph_date1"),
    url(r'^open-graph-date2$', 'app.market.test.views.open_graph_date2', name="open_graph_date2"),)
