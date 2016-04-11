# -*- coding: utf-8 -*-
import csv

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


class TrackingChangeList(ChangeList):
    def get_results(self, request):
        super(TrackingChangeList, self).get_results(request)
        self.result_list = self.model_admin.make_tracking_queryset(
            self.result_list)


class TrackingAdmin(admin.ModelAdmin):

    EXPORT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_changelist(self, request, **kwargs):
        return TrackingChangeList

    # Overridden methods.

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST':
            if '_export' in request.POST:
                return self.export_as_csv(request)
        return super(TrackingAdmin, self).changelist_view(request,
                                                          extra_context)

    # Utils.

    @staticmethod
    def make_tracking_queryset(orig_queryset):
        raise NotImplementedError

    def _prep_field(self, obj, field):
        """
        Returns the field as a unicode string. If the field is a callable,
        it attempts to call it first.
        """
        attr = getattr(self, field, None)
        if callable(attr):
            attr = attr(obj)
        else:
            attr = getattr(obj, field)
        return unicode(attr).replace('\n', ' ')\
            .replace('\r', '')\
            .replace(';', ',')\
            .encode('utf-8')

    def _get_labels(self, field_names):
        def _get_model_attr():
            return getattr(self.model, label)
        return [getattr(getattr(self, label, _get_model_attr),
                'short_description', label) for label in field_names]

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

        labels = self._get_labels(field_names)

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s%s.csv' % (
            unicode(opts).replace('.', '_'), extra_file_name
        )

        writer = csv.writer(response, delimiter=';')

        if header:
            writer.writerow([unicode(label).capitalize() for label in labels])

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)
        ChangeList = self.get_changelist(request)
        cl = ChangeList(request, self.model, list_display,
                        list_display_links, list_filter, self.date_hierarchy,
                        self.search_fields, self.list_select_related,
                        self.list_per_page, self.list_max_show_all, self.list_editable,
                        self)

        queryset = self.make_tracking_queryset(cl.get_queryset(request))
        for obj in queryset:
            fields = []
            for field in field_names:
                try:
                    fields.append(self._prep_field(obj, field))
                except ObjectDoesNotExist:
                    fields.append('')
            writer.writerow(fields)
        return response

    def __init__(self, *args, **kwargs):
        super(TrackingAdmin, self).__init__(*args, **kwargs)
        self.user_model = get_user_model()
