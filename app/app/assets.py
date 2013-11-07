from django_assets import register,Bundle
from unipath import Path
from django.conf import settings

js = Bundle(
    Bundle(
        './js/lib/modernizr.custom.18630.js',
        './js/lib/jquery-1.10.2.min.js',
        './js/lib/underscore-min.js',
        './js/lib/backbone-min.js',        
        './js/lib/jquery.ui.position.js',
        './js/lib/moment-with-langs.min.js',
        './js/lib/bootstrap.js',
        './js/lib/bootstrap-datetimepicker.min.js',        
        './js/lib/typeahead.min.js',
        './js/lib/tagmanager.js',
        ),
    filters='jsmin',
    output='./js/packed.js'
)

if settings.PRODUCTION:

    css = Bundle(
        # './css/cssreset-min.css',        
        './css/bootstrap.css',
        './css/bootstrap-datetimepicker.min.css',
        './css/tagmanager.css',
        './css/typeahead.css',
        # './css/bootstrap-theme.css',        
        './css/site.css',
        filters='cssmin',
        output='./css/packed.css'
    )

else:

    css = Bundle(
        Bundle(
            # './css/cssreset-min.css',
            './css/bootstrap.css',
            './css/bootstrap-datetimepicker.min.css',
            './css/tagmanager.css',
            './css/typeahead.css',
            #'./css/bootstrap-theme.css',            
            ),
        Bundle(
            './css/site.styl',
            filters='stylus',
            output ='./css/site.css'
            ),
        filters='cssmin',
        output='./css/packed.css'
    )

register('js_all', js)
register('css_all', css)


