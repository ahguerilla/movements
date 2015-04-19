from operator import itemgetter


def form_errors_as_dict(form):
    return dict((k, map(unicode, v)) for (k, v) in form.errors.iteritems())


class EnumChoices(list):
    """
    A helper to create constants from choices tuples.

    Usage:
    CONNECTION_CHOICES = EnumChoices(
        WIRED    = (1, 'Wired connection'),
        WIRELESS = (2, 'Wi-fi or other generic wireless type'),
        MOBILE   = (3, 'Mobile broadband'),
    )

    It will then return a list with the passed tuples so you can use in the
    Django's fields choices option and, additionally, the returned object will
    have the constant names as attributes (eg. CONNECTION_CHOICES.MOBILE == 3).
    """
    def __init__(self, **data):
        for item in sorted(data.items(), key=itemgetter(1)):
            self.append((item[1][0], item[1][1]))
            setattr(self, item[0], item[1][0])
