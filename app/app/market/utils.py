# -*- coding: utf-8 -*-
import csv
from django.http import HttpResponse


def prep_field(obj, field):
    """ Returns the field as a unicode string. If the field is a callable, it
    attempts to call it first, without arguments.
    """
    if '__' in field:
        bits = field.split('__')
        field = bits.pop()

        for bit in bits:
            obj = getattr(obj, bit, None)

            if obj is None:
                return ""

    attr = getattr(obj, field)
    output = attr() if callable(attr) else attr
    return unicode(output).encode('utf-8')


def export_as_csv(model_admin, queryset, header=True):
    opts = model_admin.model._meta
    field_names = [f.name for f in opts.fields]
    field_names = list(model_admin.list_display) + field_names

    if model_admin.csv_field_exclude:
        field_names = [f for f in field_names
                       if not f in model_admin.csv_field_exclude]

    labels = [
        getattr(
            model_admin.model.__dict__.get(label, label),
            'short_description', label) for label in field_names]

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
        unicode(opts).replace('.', '_')
    )

    writer = csv.writer(response, delimiter=';')

    if header:
        writer.writerow([unicode(label).capitalize() for label in labels])

    for obj in queryset:
        writer.writerow([prep_field(obj, field) for field in field_names])
    return response
