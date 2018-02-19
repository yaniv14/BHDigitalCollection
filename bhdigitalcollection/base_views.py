from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _


class BHUIMixin(object):
    page_title = None
    page_name = None
    filterable = False

    filters_types = {
        '': None,
        'time': _('Period'),
        'location': _('Area'),
    }

    def set_filters(self):
        return None

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        return ""

    def get_page_name(self):
        if self.page_name:
            return self.page_name
        return ""

    def get_filterable(self):
        return self.filterable

    def is_msie(self):
        if settings.DEBUG:
            return True
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        return 'MSIE' in user_agent or 'Trident' in user_agent

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['page_title'] = self.get_page_title()
        d['page_name'] = self.get_page_name()
        d['filterable'] = self.get_filterable()
        d['filter'] = self.set_filters()
        d['filter_type'] = self.filters_types.get(self.request.GET.get('filter', ''))
        d['current_url_name'] = self.request.resolver_match.url_name
        return d


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='users:login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
