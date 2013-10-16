from django.contrib import admin
from models import Placeholder

class PlaceholderAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'screen':('http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css',)
        }
        js = (
            'js/lib/jquery-1.10.2.min.js' ,
            'http://code.jquery.com/ui/1.10.3/jquery-ui.js'
        )
    list_display = ('location', 'content')

admin.site.register(Placeholder, PlaceholderAdmin)
