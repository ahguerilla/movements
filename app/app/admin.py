# -*- coding: utf-8 -*-
import csv
import json
import re
from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.mail import EmailMessage

from adminsortable2.admin import SortableAdminMixin
from cms.extensions import PageExtensionAdmin

from .models import NewsletterSignups, MenuExtension, NotificationPing, Partner
from .celerytasks import notification_ping

from django.contrib.auth.models import User, Group
import django.db as db

from django.conf import settings
from django.template.loader import render_to_string
from app.users.models import UserProfile
from app.market.models import MarketItem
import constance


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
def notification_ping(request):
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
    change_list_template = 'admin/group_user_management_list.html'
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(GroupUserAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def user_groups(self, obj):
        return u", ".join([g.name for g in obj.groups.all()])

    def has_add_permission(self, request):
        return False

    def has_edit_permission(self, request):
        return False

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=group_users.csv'
            writer = csv.writer(response, delimiter=';')
            headers = ['UserId', 'Username', 'FirstName', 'LastName', 'Email', 'Groups']
            writer.writerow([unicode(label).capitalize() for label in headers])

            # this allows us to get the filtered queryset
            list_display = self.get_list_display(request)
            list_display_links = self.get_list_display_links(request, list_display)
            list_filter = self.get_list_filter(request)
            ChangeList = self.get_changelist(request)
            cl = ChangeList(request, self.model, list_display,
                            list_display_links, list_filter, self.date_hierarchy,
                            self.search_fields, self.list_select_related,
                            self.list_per_page, self.list_max_show_all, self.list_editable,
                            self)

            qs = cl.get_queryset(request)
            for r in qs.iterator():
                fields = [r.id, r.username.encode('utf8'), r.first_name.encode('utf8'), r.last_name.encode('utf8'),
                          r.email, u", ".join([g.name for g in r.groups.all()])]
                writer.writerow(fields)
            return response
        return super(GroupUserAdmin, self).changelist_view(request, extra_context)


class GroupManagementManager(db.models.Manager):
    def __init__(self):
        super(GroupManagementManager, self).__init__()

    def get_query_set(self):
        return super(GroupManagementManager, self).get_query_set()


class GroupManagement(Group):
    class Meta:
        proxy = True
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    objects = GroupManagementManager()


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'members', 'manage',)
    exclude = ('permissions',)

    def __init__(self, *args, **kwargs):
        super(GroupAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = (None, )

    def members(self, obj):
        return obj.user_set.count()

    def manage(self, obj):
        update_link = u'<a href="{0}">update >></a>'.format(
            reverse('admin:app_groupmanagement_change', args=(obj.id,)))
        message_link = u'<a href="{0}">send message >></a>'.format(
            reverse('admin:group_email', args=(obj.id,)))
        return update_link + u'&nbsp;&nbsp;&nbsp;' + message_link
    manage.allow_tags = True


@admin.site.register_view('group-email/(?P<group_id>\d+)', urlname='group_email')
def group_email(request, group_id):
    group = Group.objects.get(pk=group_id)
    return render(request, 'admin/group_email.html', {'group': group})


@admin.site.register_view('group-email/send/(?P<group_id>\d+)/test$', urlname='group_email_test')
def group_email_test(request, group_id):
    if request.method == 'POST':
        try:
            group = Group.objects.get(pk=group_id)
            if not group:
                raise ValueError("Invalid group")
            message = request.POST.get('message')
            if not message:
                raise ValueError("Please enter a valid message")
            email_to = request.POST.get('email_to')
            if not email_to:
                raise ValueError("Please enter a valid email")
            message = construct_email(message, request.user, group)
            send_group_email(message, request.user, email_to)
        except Exception as ex:
            return HttpResponse(json.dumps({'success': False, 'message': ex.message}), mimetype="application/json")
        success_message = 'successfully sent a test message to {0}'.format(email_to)
        return HttpResponse(json.dumps({'success': True, 'message': success_message}), mimetype="application/json")
    return HttpResponseNotAllowed('Invalid method')


@admin.site.register_view('group-email/send/(?P<group_id>\d+)$', urlname='group_email_send')
def group_email_send(request, group_id):
    if request.method == 'POST':
        success_count = 0
        try:
            group = Group.objects.get(pk=group_id)
            if not group:
                raise ValueError("Invalid group")
            message = request.POST.get('message')
            if not message:
                raise ValueError("Please enter a valid message")
            for u in group.user_set.all():
                message = construct_email(message, u, group)
                send_group_email(message, u)
                success_count += 1
        except Exception as ex:
            return HttpResponse(json.dumps({'success': False, 'message': ex.message}), mimetype="application/json")
        success_message = 'successfully sent message to {0} users'.format(success_count)
        return HttpResponse(json.dumps({'success': True, 'message': success_message}), mimetype="application/json")
    return HttpResponseNotAllowed('Invalid method')


def construct_email(message, user, group):
    full_name = (user.first_name + u' ' + user.last_name).strip()
    full_name = full_name if full_name else u'Movements.Org user'
    first_name = user.first_name.strip()
    first_name = first_name if first_name else u'Movements.Org user'
    last_name = user.last_name.strip()
    message = message.replace(u'##FULL_NAME##', full_name)
    message = message.replace(u'##FIRST_NAME##', first_name)
    message = message.replace(u'##LAST_NAME##', last_name)
    profile = UserProfile.objects.get(user=user)
    posts_matched = re.findall(r'##POST_ID=\d+##', message)
    for post in posts_matched:
        post_id = post.split(u'=')[1][:-2]
        try:
            market_item = MarketItem.objects.get(pk=post_id)
        except Exception as ex:
            raise ValueError("Invalid post id specified {0}".format(post_id))
        url = settings.BASE_URL + reverse('show_post', args=[post_id])
        html_url = '<a href="' + url + '">' + url + '</a>'
        message = message.replace(post, html_url)
    template_args = {
        'base_url': settings.BASE_URL,
        'unsub_uuid': profile.get_unsubscribe_uuid(),
        'group_id': group.id,
        'group_name': group.name,
    }
    footer = render_to_string('emails/snippets/_group_email_notification_settings.html', template_args)
    message_parts = message.split(u'##NOTIFICATION_PREFERENCES##')
    message_list = []
    for m in message_parts:
        paragraphs_list = []
        paragraphs = m.split('\n')
        for p in paragraphs:
            p = p.strip()
            if p:
                paragraphs_list.append('<p>' + p + '</p>')
        message_list.append('\n'.join(paragraphs_list))

    message = ''
    first = True
    for i in message_list:
        if not first:
            message += '\n' + footer + '\n'
        first = False
        message += '\n' + i + '\n'
    return message


def send_group_email(message, user, email_to=''):
    to_address = email_to if email_to else user.email
    email = EmailMessage(
        'Group message from Movements.Org',
        message,
        constance.config.NO_REPLY_EMAIL,
        [to_address]
    )
    email.content_subtype = "html"
    email.send()


admin.site.register(GroupUser, GroupUserAdmin)
admin.site.register(GroupManagement, GroupAdmin)