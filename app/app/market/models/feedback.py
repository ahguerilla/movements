# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from app.utils import EnumChoices


class Question(models.Model):
    TYPE_CHOICES = EnumChoices(
        YESNO=(0, _('Yes/No')),
        RANGE=(1, _('Range (1-5)')),
        TEXT_LONG=(2, _('Free Text Long')),
        TEXT_SHORT=(3, 'Free Text Short')
    )

    question = models.TextField(_('question'))
    question_type = models.PositiveSmallIntegerField(
        _('question type'), null=True, blank=True, choices=TYPE_CHOICES)

    class Meta:
        app_label = 'market'
        verbose_name = _('question configuration')
        verbose_name_plural = _('question configurations')

    def __unicode__(self):
        return u'%s / %s' % (
            self.question, self.get_question_type_display() or
            _('without type'))


class Questionnaire(models.Model):
    title = models.CharField(_('title'), max_length=255)
    questions = models.ManyToManyField(
        Question, verbose_name=_('questions'))

    class Meta:
        app_label = 'market'
        verbose_name = _('questionnaire')
        verbose_name_plural = _('questionnaires')

    def __unicode__(self):
        return u'%s' % self.title
