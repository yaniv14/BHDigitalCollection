from authtools.views import LoginView
from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from jewishdiaspora.base_views import JewishDiasporaUIMixin
from users.forms import ContactForm, LoginForm, MyUserAccount
from users.models import ArtifactContact
from jewishdiaspora.base_views import JewishDiasporaUIMixin, LoginRequiredMixin


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


class MyAccount(LoginRequiredMixin, SuccessMessageMixin, JewishDiasporaUIMixin, FormView):
    template_name = 'users/my_account.html'
    form_class = MyUserAccount
    success_url = reverse_lazy('users:my_account')
    page_title = _('Account Update')
    page_name = 'account_update'
    success_message = _('Your account was updated successfully')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'logged': self.request.user.is_authenticated,
            'bidi': translation.get_language_bidi()
        })
        return kwargs

    def get_initial(self):
        return {
            'phone_number': self.request.user.phone,
            'full_name': self.request.user.full_name,
            'email': self.request.user.email,
        }

    def form_valid(self, form):
        user = self.request.user
        user.phone= form.cleaned_data['phone_number']
        user.full_name = form.cleaned_data['full_name']
        if form.cleaned_data.get('password'):
            user.set_password(form.cleaned_data.get('password'))
        user.save()
        login(self.request, user)

        return super().form_valid(form)


