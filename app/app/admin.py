from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.core.urlresolvers import reverse

from adminsortable2.admin import SortableAdminMixin
from cms.extensions import PageExtensionAdmin

from .models import NewsletterSignups, MenuExtension, NotificationPing, Partner
from .celerytasks import notification_ping

from django.contrib.auth.models import User
import django.db as db



class MenuExtensionAdmin(PageExtensionAdmin):
    pass


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = LogEntry._meta.get_all_field_names()
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]
    search_fields = [
        'object_repr',
        'change_message'
    ]
    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        try:
            if obj.action_flag == DELETION:
                link = escape(obj.object_repr)
            else:
                ct = obj.content_type
                link = u'<a href="%s">%s</a>' % (
                    reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                    escape(obj.object_repr),
                )
            return link
        except:
            return "link unavailable"
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
    
    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')



@admin.site.register_view('market/testing/notification_ping', urlname="notification_ping")
def process_buy_orders(request):
    if request.method == 'POST':
        email_to = request.POST.get('email_to', None)
        if not email_to:
            email_to = request.user.email
        notification_ping.delay(email_to)
        return redirect(reverse('admin:app_notificationping_changelist'))
    return render(request, 'admin/testing/notification_ping.html', {})


class SortableAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(MenuExtension, MenuExtensionAdmin)
admin.site.register(NewsletterSignups)
admin.site.register(NotificationPing)
admin.site.register(Partner, SortableAdmin)
admin.site.register(LogEntry, LogEntryAdmin)


class GroupUserManager(db.models.Manager):
    def __init__(self):
        super(GroupUserManager, self).__init__()

    def get_query_set(self):
        return super(GroupUserManager, self).get_query_set()


class GroupUser(User):
    class Meta:
        proxy = True
        verbose_name_plural = 'Groups and Users'
    objects = GroupUserManager()


class GroupUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_groups')
    list_filter = ('groups',)

    def __init__(self, *args, **kwargs):
        super(GroupUserAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def user_groups(self, obj):
        return u", ".join([g.name for g in obj.groups.all()])

    def has_add_permission(self, request):
        return False

    def has_edit_permission(self, request):
        return False


admin.site.register(GroupUser, GroupUserAdmin)