from django.conf import settings
from django_assets import register,Bundle


js = Bundle(
    Bundle(
        './js/lib/jquery-1.10.2.min.js',
        './js/lib/underscore-min.js',
        './js/lib/backbone-min.js',
        './js/lib/jquery.ui.position.js',
        './js/lib/moment-with-langs.min.js',
        './js/lib/moment-timezone.min.js',
        './js/lib/bootstrap.js',
        './js/lib/bootstrap-datetimepicker.min.js',
        './js/lib/tagmanager.js',
        './js/lib/typeahead.min.js',
        './js/lib/jquery.blockUI.js',
        './js/lib/jstz.js',
        './js/lib/jquery.backstretch.min.js',
        './js/lib/masonry.pkgd.js',
        './js/app_common.js',
        './js/base.js',
        './js/item_form_base.js',
        './js/offer_form.js',
        './js/request_form.js',
        './js/marketbase.js',
        './js/market.js',
        './js/users.js',
        './js/item_single.js',
        './js/messages.js',
        './js/comment.js',
        './js/posts.js',
        './js/lib/jquery.rateit.min.js',
        ),
    filters='jsmin',
    output='./js/packed.js'
)

if settings.PRODUCTION or settings.STAGING:
    css = Bundle(
        './css/bootstrap.css',
        './css/bootstrap-datetimepicker.min.css',
        './css/tagmanager.css',
        './css/typeahead.css',
        './css/rateit.css',
        './css/site.css',
        filters='cssmin',
        output='./css/packed.css'
    )
else:
    css = Bundle(
        Bundle(
            './css/bootstrap.css',
            './css/bootstrap-datetimepicker.min.css',
            './css/tagmanager.css',
            './css/typeahead.css',
            './css/rateit.css'
            ),
        Bundle(
            './css/site.styl',
            './css/market.styl',
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
