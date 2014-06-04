import csv

from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.main import ChangeList
from app.users.models import (
    UserProfile, Countries, Skills, Issues, Nationality, UserTracking)
from django.contrib.admin.models import LogEntry
from modeltranslation.admin import TranslationAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'vetting' ,'vetted_by')

    def vetting(self, obj):
        if obj.is_staff:
            return 'Staff'
        result = 'Vetted' if obj.is_active else 'Not Vetted'
        vet_url = reverse('vet_user', args=(obj.id,))
        return u'<a href="{0}" target="_blank" alt="vet user">Vet User</a> ({1})'.format(vet_url, result)
    vetting.process = 'Process'
    vetting.allow_tags = True

    def vetted_by(self,obj):
        log = LogEntry.objects.filter(object_id = obj.id).all()
        if len(log)>0:
            return log[0].user.username
        else:
            return ''

class SkillsAdmin(TranslationAdmin):
    list_display = ('skills',)

class CountriesAdmin(TranslationAdmin):
    list_display = ('countries',)

class IssuesAdmin(TranslationAdmin):
    list_display = ('issues',)

class NationalityAdmin(TranslationAdmin):
    list_display = ('nationality',)


class TrackingChangeList(ChangeList):
    def get_results(self, request):
        super(TrackingChangeList, self).get_results(request)
        self.result_list = self.model_admin.make_tracking_queryset(
            self.result_list)


class UserTrackingAdmin(admin.ModelAdmin):
    list_select_related = ('userprofile',)
    list_display = (
        'id', 'get_screen_name', 'get_signup_date', 'get_full_name',
        'get_nationality', 'get_resident_country', 'email',
        'get_request_count', 'get_offer_count', 'get_comment_count',
        'last_login', 'is_admin'
    )
    change_list_template = 'admin/tracking_change_list.html'
    csv_field_exclude = (
        'is_superuser', 'password', 'username', 'is_staff', 'fullname',
        'is_active', 'first_name', 'last_name')
    csv_safe_fields = csv_field_exclude + (
        'get_full_name', 'email')

    # Prepare fields for change list and CSV.

    def get_screen_name(self, obj):
        return obj.username
    get_screen_name.short_description = _('Screen Name')

    def get_signup_date(self, obj):
        return obj.date_joined
    get_signup_date.short_description = _('Signup Date')

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _('Full Name')

    def get_nationality(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.nationality
        return ''
    get_nationality.short_description = _('Nationality')

    def get_resident_country(self, obj):
        if hasattr(obj, 'userprofile'):
            return obj.userprofile.resident_country
        return ''
    get_resident_country.short_description = _('Country of Residence')

    def is_admin(self, obj):
        return obj.is_staff
    is_admin.short_description = _('Is Admin')

    def get_request_count(self, obj):
        return obj.request_count
    get_request_count.short_description = _('Request Count')

    def get_offer_count(self, obj):
        return obj.offer_count
    get_offer_count.short_description = _('Offer Count')

    def get_comment_count(self, obj):
        return obj.comment_count
    get_comment_count.short_description = _('Comment Count')

    # Overridden methods.

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist(self, request, **kwargs):
        return TrackingChangeList

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            if '_export' in request.POST:
                return self.export_as_csv(request)
            elif '_safe_export' in request.POST:
                return self.export_as_csv(request, safe_mode=True)
        return super(UserTrackingAdmin, self).changelist_view(request,
                                                              extra_context)

    # Utils.

    @staticmethod
    def make_tracking_queryset(orig_queryset):
        queryset = orig_queryset.annotate(
            comment_count=Count('comment', distinct=True)
        )
        request_count_dict = dict(orig_queryset.filter(
            marketitem__item_type='request').annotate(
                request_count=Count('marketitem')
            ).values_list('id', 'request_count'))
        offer_count_dict = dict(orig_queryset.filter(
            marketitem__item_type='offer').annotate(
                offer_count=Count('marketitem')
            ).values_list('id', 'offer_count'))

        users = queryset[:]
        for user in users:
            user.request_count = request_count_dict.get(user.id, 0)
            user.offer_count = offer_count_dict.get(user.id, 0)
        return users

    def _prep_field(self, obj, field):
        """
        Returns the field as a unicode string. If the field is a callable,
        it attempts to call it first.
        """
        attr = getattr(self, field, None)
        if attr:
            attr = attr(obj)
        else:
            attr = getattr(obj, field)
        return unicode(attr).encode('utf-8')

    def export_as_csv(self, request, header=True, safe_mode=False):
        extra_file_name = ''
        opts = self.model._meta
        field_names = [f.name for f in opts.fields]
        field_names = list(self.list_display) + field_names
        # Make unique sequence with ordering.
        unique = set()
        unique_add = unique.add
        field_names = [x for x in field_names
                       if x not in unique and not unique_add(x)]

        if hasattr(self, 'csv_field_exclude'):
            field_names = [f for f in field_names
                           if not f in self.csv_field_exclude]

        if safe_mode:
            extra_file_name = '_safe'
            if hasattr(self, 'csv_safe_fields'):
                field_names = [f for f in field_names
                               if not f in self.csv_safe_fields]

        def _get_model_attr():
            return getattr(self.model, label)

        labels = [
            getattr(getattr(self, label, _get_model_attr),
                    'short_description', label) for label in field_names]

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s%s.csv' % (
            unicode(opts).replace('.', '_'), extra_file_name
        )

        writer = csv.writer(response, delimiter=';')

        if header:
            writer.writerow([unicode(label).capitalize() for label in labels])

        queryset = self.make_tracking_queryset(self.get_queryset(request))
        for obj in queryset:
            writer.writerow([self._prep_field(obj, field)
                             for field in field_names])
        return response


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Countries, CountriesAdmin)
admin.site.register(Skills, SkillsAdmin)
admin.site.register(Issues, IssuesAdmin)
admin.site.register(Nationality, NationalityAdmin)

admin.site.register(UserTracking, UserTrackingAdmin)
