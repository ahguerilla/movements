from modeltranslation.translator import translator, TranslationOptions
from app.users.models import (
    Countries, Skills, Issues, Nationality, Residence,
    Language, Region, Interest)
from app.models import HomePageBanner


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


class HomePageBannerOptions(TranslationOptions):
    fields = ('title_text', 'sub_text',)


class NamedObjectTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Residence, ResidenceTranslationOptions)
translator.register(Countries, CountriesTranslationOptions)
translator.register(Nationality, NationalityTranslationOptions)
translator.register(Skills, SkillsTranslationOptions)
translator.register(Issues, IssuesTranslationOptions)
translator.register(HomePageBanner, HomePageBannerOptions)

translator.register(Language, NamedObjectTranslationOptions)
translator.register(Region, NamedObjectTranslationOptions)
translator.register(Interest, NamedObjectTranslationOptions)
