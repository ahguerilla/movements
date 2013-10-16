from django import template
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ..models import Placeholder

register = template.Library()

from django_jinja import library
jregister  = library.Library()

@register.tag(name="editable")
def do_editable(parser, token):
    try:
        tag_name, tag_argument = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument." % token.contents.split()[0])
    if not(tag_argument[0] == tag_argument[-1] and tag_argument[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's arguments should be in quotes." % tag_name)
    return EditableNode(tag_argument)


class EditableNode(template.Node):

    def __init__(self, tag_argument):
        self.tag_arg = tag_argument.encode('utf-8').strip("'").strip('"')
        self.logout_url = reverse('logout')
        self.edit_url = reverse('edit', args=[self.tag_arg])

    def render(self, context):
        if self.tag_arg == 'admin':
            if context['user'].is_authenticated():
                return """<div id="admin_bar"><p>You are now logged in as '%s'.<br/> Click to <a href=%s>Logout</a></p></div>""" % (context['user'], self.logout_url)
            else:
                return ""

        else:
            obj = Placeholder.objects.filter(location=self.tag_arg)
            if context['user'].is_authenticated():
                for x in obj:
                    return "%s<br/><a href=%s>edit</a>" % (x, self.edit_url)
            else:
                for x in obj:
                    return x


@jregister.global_function
def editable(tag_argument,request):
    return JEditableNode(tag_argument).render(request)


class JEditableNode(template.Node):

    def __init__(self, tag_argument):
        self.tag_arg = tag_argument.encode('utf-8')
        self.logout_url = reverse('logout')
        self.edit_url = reverse('edit', args=[self.tag_arg])

    def render(self, request):
        if self.tag_arg == 'admin':
            if request.user.is_authenticated():
                return """<div id="admin_bar"><p>You are now logged in as '%s'.<br/> Click to <a href=%s>Logout</a></p></div>""" % (request.user, self.logout_url)
            else:
                return ""

        else:
            obj = Placeholder.objects.filter(location=self.tag_arg)
            if len(obj)==0:
                return "location '%s'"%self.tag_arg
            if request.user.is_authenticated():
                for x in obj:
                    if x.noinline:
                        return unicode(x)
                    else:
                        return u"%s<a class='editablelink' href=%s?redirectaddr=%s>edit</a>" % (x, self.edit_url,request.get_full_path())
            else:
                for x in obj:
                    return x