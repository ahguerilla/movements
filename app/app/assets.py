from django_assets import register
from webassets.ext.jinja2 import Bundle
from unipath import Path
from django.conf import settings

from django_jinja.base import env as Jinja2Environment
from webassets import Environment as AssetsEnvironment

PROJECT_DIR = Path(__file__).ancestor(2)
assets_env = AssetsEnvironment(PROJECT_DIR.child("static"),)
assets_env.url = settings.ASSETS_URL
assets_env.debug = settings.ASSETS_DEBUG
Jinja2Environment.assets_environment = assets_env


if settings.PRODUCTION:

	js = Bundle(
		Bundle(
		    './js/lib/modernizr.custom.18630.js',
		    './js/lib/jquery-1.10.2.min.js',
		    './js/lib/underscore-min.js',
		    './js/lib/backbone-min.js',
		    './js/lib/jquery.contextMenu.js',
		    './js/lib/jquery.ui.position.js',
		    ),
		Bundle(
		    './js/lib/editable.js',
		    ),
		filters='jsmin',
		output='./js/packed.js'
	)

	css = Bundle(
	    './css/cssreset-min.css',
	    './css/jquery.contextMenu.css',
	    './css/site.css',
	    filters='cssmin',
	    output='./css/packed.css'
	)

else:

	js = Bundle(
		Bundle(
		    './js/lib/modernizr.custom.18630.js',
		    './js/lib/jquery-1.10.2.min.js',
		    './js/lib/underscore-min.js',
		    './js/lib/backbone-min.js',
		    './js/lib/jquery.contextMenu.js',
		    './js/lib/jquery.ui.position.js',
		    ),
		Bundle(
		    './js/lib/editable.js',
		    ),
		filters='jsmin',
		output='./js/packed.js'
	)

	css = Bundle(
		Bundle(
		    './css/cssreset-min.css',
		    './css/jquery.contextMenu.css',
		    ),
		Bundle(
		    './css/site.styl',
		    filters='stylus',
		    output ='./css/site.css'
		    ),
		filters='cssmin',
		output='./css/packed.css'
	)

assets_env.register('js_all', js)
assets_env.register('css_all', css)


