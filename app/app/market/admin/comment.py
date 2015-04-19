from django.contrib import admin
import app.market.models as models
import django.db as db

class CommentAdmin(admin.ModelAdmin):
    list_display = ('contents', 'pub_date', 'published',)
    pass

admin.site.register(models.Comment, CommentAdmin)
