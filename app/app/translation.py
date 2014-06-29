from modeltranslation.translator import translator, TranslationOptions
from app.users.models import (
    Countries, Skills, Issues, Nationality, Residence,
    Language, Region, Interest)

class ResidenceTranslationOptions(TranslationOptions):
    fields = ('residence',)

class CountriesTranslationOptions(TranslationOptions):
    fields = ('countries',)

class NationalityTranslationOptions(TranslationOptions):
    fields = ('nationality',)

class SkillsTranslationOptions(TranslationOptions):
    fields = ('skills',)

class IssuesTranslationOptions(TranslationOptions):
    fields = ('issues',)

class PlaceholderTranslationOptions(TranslationOptions):
    fields = ('content',)


class NamedObjectTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Residence, ResidenceTranslationOptions)
translator.register(Countries, CountriesTranslationOptions)
translator.register(Nationality, NationalityTranslationOptions)
translator.register(Skills, SkillsTranslationOptions)
translator.register(Issues, IssuesTranslationOptions)

translator.register(Language, NamedObjectTranslationOptions)
translator.register(Region, NamedObjectTranslationOptions)
translator.register(Interest, NamedObjectTranslationOptions)
