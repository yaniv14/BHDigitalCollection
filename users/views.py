from authtools.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.utils.translation import ugettext as _
from jewishdiaspora.base_views import JewishDiasporaUIMixin
from users.forms import ContactForm, LoginForm
from users.models import ArtifactContact


class ContactView(JewishDiasporaUIMixin, SuccessMessageMixin, CreateView):
    template_name = 'users/contact_form.html'
    model = ArtifactContact
    success_url = reverse_lazy('contact')
    page_title = _('Contact us')
    page_name = 'contact_us'
    form_class = ContactForm
    success_message = _('Thank you, we will contact you shortly')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class BHLoginView(LoginView):
    form_class = LoginForm
