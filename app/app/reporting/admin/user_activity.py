# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ..models import UserActivity


class UserActivityAdmin(admin.ModelAdmin):
    list_select_related = ('user',)
    date_hierarchy = 'action_time'
    list_display = ('user', 'action_time', 'get_action_flag', 'get_staff_status')
    list_filter = ('user__is_staff',)
    readonly_fields = ('user', 'action_time', 'get_staff_status', 'get_action_flag')
    fields = ('user', 'action_time', 'get_staff_status', 'get_action_flag')

    def get_queryset(self, request):
        return super(UserActivityAdmin, self).get_queryset(request).filter(
            action_flag=UserActivity.ACTION_CHOICES.LOGGED_IN)

    def get_staff_status(self, obj):
        return obj.user.is_staff
    get_staff_status.short_description = _('Staff status')
    get_staff_status.admin_order_field = 'user__is_staff'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(UserActivity, UserActivityAdmin)
