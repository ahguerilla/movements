from django.db import models
from django.forms import ModelForm
from django import forms

class Placeholder(models.Model):
    location = models.SlugField(max_length=50, unique=True, help_text=
                                """This field must match the argument given in {% editable %} tag. Use only letters, number, underscores or hyphens only. Must be a unique name""")
    content = models.TextField(max_length=1500, help_text="Add any text you like!")
    noinline = models.BooleanField('Disable live Edit',default=False)

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['location']


class EditForm(ModelForm):
    redirectaddr = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Placeholder
        fields = ['content','redirectaddr']
