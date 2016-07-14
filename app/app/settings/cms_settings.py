"""CMS Settings."""
_ = lambda s: s

CMS_PERMISSION = True

CMS_PLUGIN_CACHE = False
CMS_PAGE_CACHE = False
CMS_PLACEHOLDER_CACHE = False

CMS_CACHE_DURATIONS = {
    'content': 3600,
    'menus': 3600,
    'permissions': 3600,
}

CMS_TEMPLATES = (
    ('cms/single_page.html', 'Single Page'),
    ('cms/page_with_left_nav.html', 'Page With Left Nav'),
)

CMS_PLACEHOLDER_CONF = {
    'title':{
        'plugins': ['TextPlugin',],
    },
}

# Reverse id for cms pages.
CMS_PAGE_TERMS = 'terms-and-conditions'

# Don't allow the CMS Toolbar to display when not logged in
CMS_TOOLBAR_ANONYMOUS_ON = False