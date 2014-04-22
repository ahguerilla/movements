from threading import Lock

from django.core.cache import cache
from django.db.models import Q

from cms.models import Page
from menus.base import Modifier
from menus.menu_pool import menu_pool


menu_lock = Lock()


def invalidate_menu_cache():
    cache.delete_many(['top_level_menu_ids', 'footer_menu_ids'])


def get_from_cache():
    cache_res = cache.get_many(['top_level_menu_ids', 'footer_menu_ids'])
    tlm = cache_res.get('top_level_menu_ids')
    fm = cache_res.get('footer_menu_ids')
    return tlm, fm


def load_menu_settings():
    tlm, fm = get_from_cache()
    if tlm and fm:
        return tlm, fm
    with menu_lock:
        tlm, fm = get_from_cache()
        if tlm and fm:
            return tlm, fm
        tlm = set()
        fm = set()
        pages = Page.objects.filter(
            Q(menuextension__show_on_top_menu=True) |
            Q(menuextension__show_on_footer_menu=True))\
            .select_related('menuextension')\
            .all()
        for page in pages:
            if page.menuextension.show_on_top_menu:
                tlm.add(page.id)
            if page.menuextension.show_on_footer_menu:
                fm.add(page.id)
        cache.set_many({
            'top_level_menu_ids': tlm,
            'footer_menu_ids': fm,
        })
        return tlm, fm


class MenuMarker(Modifier):
    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        tlm, fm = load_menu_settings()
        if post_cut:
            return nodes
        for node in nodes:
            if node.id in tlm:
                node.show_in_top_menu = True
            if node.id in fm:
                node.show_in_footer = True
        return nodes

menu_pool.register_modifier(MenuMarker)
