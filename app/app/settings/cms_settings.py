"""CMS Settings."""
_ = lambda s: s

CMS_PERMISSION = True

CMS_PLUGIN_CACHE = True
CMS_PAGE_CACHE = True
CMS_PLACEHOLDER_CACHE = True

CMS_CACHE_DURATIONS = {
    'content': 3600,
    'menus': 3600,
    'permissions': 3600,
}

CMS_TEMPLATES = (
    ('cms/single_page.html', 'Single Page'),
    ('cms/page_with_left_nav.html', 'Page With Left Nav'),
    ('cms/empty.html', 'Empty page'),
)

CMS_PLACEHOLDER_CONF = {
    'title':{
        'plugins': ['TextPlugin',],
    },
}