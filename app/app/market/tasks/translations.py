from app.users.models import Language
from app.market.models.translation import get_or_create_user_translation


def create_translations_for_item(item, model):
    for code in Language.objects.exclude(launguage_code=item.language).values_list('launguage_code'):
        code = code[0]
        if code is not None:
            get_or_create_user_translation(item.id, code, model)


def mark_translations_for_update(item, model):
    pass

