from django.contrib import admin
import models


class OfferAdmin(admin.ModelAdmin):
	pass


class RequestAdmin(admin.ModelAdmin):
	pass

class ResourceAdmin(admin.ModelAdmin):
	pass


admin.site.register(models.Offer,OfferAdmin)
admin.site.register(models.Request,RequestAdmin)
admin.site.register(models.Resource,ResourceAdmin)


