"""CMS Settings."""
_ = lambda s: s

CMS_PERMISSION = True

CMS_PLUGIN_CACHE = False
CMS_PAGE_CACHE = False
CMS_PLACEHOLDER_CACHE = False

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