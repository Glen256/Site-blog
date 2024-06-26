from django.db.models import Count
from .models import *
from django.core.cache import cache

menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати пост', 'url_name': 'add_page'},
        {'title': 'Зв\'язок з адміністрацією', 'url_name': 'contact'},
        ]


class DataMixin:
    paginated_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('movie'))
            cache.set('cats', cats, 30)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
