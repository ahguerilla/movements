from django.conf import settings
from django_assets import register,Bundle


js = Bundle(
    Bundle(
        #'./js/lib/jquery-1.10.2.min.js',
        './js/lib/jquery-1.11.0.min.js',
        './js/lib/underscore-min.js',
        './js/lib/backbone-min.js',
        './js/lib/jquery.ui.position.js',
        './js/lib/moment-with-langs.min.js',
        './js/lib/moment-timezone.min.js',
        './js/lib/bootstrap.min.js',
        './js/lib/bootstrap-datetimepicker.min.js',
        './js/lib/tagmanager.js',
        './js/lib/typeahead.js',
        './js/lib/jquery.blockUI.js',
        './js/lib/jquery.mCustomScrollbar.min.js',
        './js/lib/jstz.js',
        './js/lib/jquery.backstretch.min.js',
        './js/lib/masonry.pkgd.js',
        './js/lib/jquery.cookie.js',
        './js/app_common.js',
        './js/base.js',
        './js/item_form_base.js',
        './js/marketbase.js',
        './js/market.js',
        './js/users.js',
        './js/messages.js',
        './js/posts.js',
        './js/recommendation.js',
        './js/lib/jquery.rateit.min.js',
        ),
    filters='jsmin',
    output='./js/packed.js'
)

if settings.PRODUCTION or settings.STAGING:
    css = Bundle(
        './css/lib/bootstrap.css',
        './css/lib/bootstrap-datetimepicker.min.css',
        './css/lib/tagmanager.css',
        './css/lib/typeahead.css',
        './css/lib/jquery.mCustomScrollbar.css',
        './css/lib/rateit.css',
        './css/packed.css',
        filters='cssmin',
        output='./css/spacked.css'
    )
else:
    css = Bundle(
        Bundle(
            './css/lib/bootstrap.css',
            './css/lib/bootstrap-datetimepicker.min.css',
            './css/lib/tagmanager.css',
            './css/lib/typeahead.css',
            './css/lib/jquery.mCustomScrollbar.css',
            './css/lib/rateit.css'
            ),
        Bundle(
            './css/site.styl',
            './css/site-sm.styl',
            './css/site-xs.styl',
            filters='stylus',
            output ='./css/site.css'
            ),
        filters='cssmin',
        output='./css/packed.css'
    )

register('js_all', js)
register('css_all', css)
