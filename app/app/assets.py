from django_assets import register, Bundle

from webassets.filter.jst import JST

jstFilter = JST(template_function='_.template')

js = Bundle(
    Bundle(
        './js/lib/jquery-1.11.0.min.js',
        './js/lib/underscore-min.js',
        './js/lib/backbone-min.js',
        './js/lib/moment-with-langs.min.js',
        './js/lib/moment-timezone.min.js',
        './js/lib/bootstrap.min.js',
        './js/lib/typeahead.js',
        './js/lib/jquery.cookie.js',
        './js/lib/jquery.colorbox.js',
        './js/lib/Autolinker.js',
        './js/lib/diff.js',
        './js/lib/dropzone.js',
        './js/lib/jquery.ba-bbq.min.js',
        './js/lib/jquery.backstretch.min.js',
        './colorbox/jquery.colorbox-min.js',
        './js/app_common.js',
        './js/base.js',
        './js/market.js',
        './js/messages.js',
        './js/more_about_you.js',
        './js/user_settings.js',
        './js/create_post.js',
        './js/view_post.js',
        './js/translations.js',
        './js/region_accordion_select.js',
        './js/lib/jquery.rateit.min.js',
        './js/email_confirmation.js',
        './js/signup.js',
        './js/home.js',
        Bundle(
            './js/templates/more_about_you_progress_bar.jst',
            filters=(jstFilter,),
            output='./js/templates.js'
        ),
    ),
    filters='jsmin',
    output='./js/packed.%(version)s.js'
)

css_v2 = Bundle(
    Bundle(
        './css/lib/bootstrap.css',
        './css/lib/typeahead.css',
        './css/lib/colorbox.css',
        './css/lib/rateit.css',
        './css/fonts.css',
        './colorbox/example1/colorbox.css',
    ),
    Bundle(
        './css/site_v2.styl',
        './css/site-sm_v2.styl',
        './css/site-xs_v2.styl',
        filters='stylus',
        output='./css/site_v2.css'
    ),
    filters='cssmin',
    output='./css/packed_v2.%(version)s.css',
)

language_ar = Bundle(
    Bundle(
        './css/language_ar.styl',
        filters='stylus',
        output='./css/language_ar.css'
    ),
    filters='cssmin',
    output='./css/packed_language_ar.%(version)s.css',
)

register('js_all', js)
register('css_all_v2', css_v2)
register('css_language_ar', language_ar)
