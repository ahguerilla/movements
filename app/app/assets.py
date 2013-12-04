from django.conf import settings
from django_assets import register,Bundle
from unipath import Path


js = Bundle(
    Bundle(                
        './js/lib/jquery-1.10.2.min.js',
        './js/lib/underscore-min.js',
        './js/lib/backbone-min.js',
        #'tiny_mce/tiny_mce.js',        
        './js/lib/jquery.ui.position.js',
        './js/lib/moment-with-langs.min.js',
        './js/lib/bootstrap.js',        
        './js/lib/bootstrap-datetimepicker.min.js',
        './js/lib/tagmanager.js',
        './js/lib/typeahead.min.js',               
        './js/base.js',
        './js/marketbase.js',
        './js/market.js',
        './js/users.js',         
        './js/item_single.js',
        './js/item_form.js',        
        './js/messages.js',
        './js/comment.js',        
        './js/posts.js',            
        ),
    filters='jsmin',
    output='./js/packed.js'
)

if settings.PRODUCTION:

    css = Bundle(
        './css/bootstrap.css',
        './css/bootstrap-datetimepicker.min.css',
        './css/tagmanager.css',
        './css/typeahead.css',        
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
            ),
        Bundle(
            './css/site.styl',
            './css/market.styl',
            filters='stylus',
            output ='./css/site.css'
            ),
        filters='cssmin',
        output='./css/packed.css'
    )

register('js_all', js)
register('css_all', css)


