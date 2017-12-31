from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from artifacts.forms import ArtifactForm, UserArtifactForm, ArtifactImageFormSet, OriginAreaForm, ArtifactMaterialForm, ArtifactFormImages
from artifacts.models import Artifact, ArtifactStatus, ArtifactImage, PageBanner, OriginArea, ArtifactMaterial
from jewishdiaspora.base_views import JewishDiasporaUIMixin
from users.models import User


class PersonalInformationRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_first_page.html'


class ArtifactInformationRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_second_page.html'


class ArtifactsImagesRegistrationPage(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/sign_in_third_page.html'


class TheNewForm(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/artifacts_donor_registration.html'


class HomeView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/home.html'
    page_title = _('Home')
    page_name = 'home'
    model = Artifact
    context_object_name = 'artifacts'

    def get_queryset(self):
        return super(HomeView, self).get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=False)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['bigs'] = [1, 6, 7, 12, 13, 18, 19, 24, 25, 30, 31, 36, 37, 42, 43, 48, 49]
        context['page_banner'] = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()
        return context


class AboutView(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/about.html'
    page_title = _('About')
    page_name = 'about'


class ArtifactUsersListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/users_artifact_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('Users artifacts list')
    page_name = 'users_artifact_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super(ArtifactUsersListView, self).get_queryset().filter(is_private=True)

        return super(ArtifactUsersListView, self).get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=True)


class ArtifactDetailView(JewishDiasporaUIMixin, DetailView):
    template_name = 'artifacts/artifact_detail.html'
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'


class ArtifactCreateView(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_create.html'
    form_class = UserArtifactForm
    success_url = reverse_lazy('artifacts:details')
    page_title = _('Artifact create')
    page_description = _('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras pharetra tortor nec lacus lacinia, non sodales est tristique. '
                         'Suspendisse fermentum ultrices leo. Nunc viverra egestas purus vel sagittis. Fusce iaculis enim eget elementum volutpat. '
                         'Duis et nisi purus. Vivamus tortor odio, condimentum rhoncus magna vitae, posuere tincidunt eros. Sed mollis quis ante et faucibus.')
    form_description = _('Some Personal Data')
    page_name = 'artifact_create'

    def get_initial(self):
        if self.request.user.is_authenticated:
            return {
                'name': self.request.user.full_name,
                'email': self.request.user.email,
                'phone': self.request.user.phone,
            }

    # def get(self, request):
    #     if self.request.user.is_authenticated:
    #         if self.request.user.is_superuser:
    #             return super(ArtifactUsersListView, self).get_queryset().filter(is_private=True)
    #         else:
    #             return redirect('artifacts:details')
    #     else:
    #         return super().get(self, request)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone_number')
        password = User.objects.make_random_password()

        # TODO: Send Email

        if not self.request.user.is_authenticated:
            user = User.objects.create_user(email=email, password=password, full_name=name, phone=phone)
            login(self.request, user)

        return super().form_valid(form)


class OriginAreaCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area create')
    page_name = 'origin_area_create'


class OriginAreaUpdateView(JewishDiasporaUIMixin, UpdateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class OriginAreaListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/origin_area_list.html'
    model = OriginArea
    context_object_name = 'areas'
    page_title = _('Origin area list')
    page_name = 'origin_area_list'


class ArtifactMaterialCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material create')
    page_name = 'artifact_material_create'


class ArtifactMaterialUpdateView(JewishDiasporaUIMixin, UpdateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material update')
    page_name = 'artifact_material_update'


class ArtifactMaterialDeleteView(JewishDiasporaUIMixin, DeleteView):
    template_name = 'artifacts/artifact_material_delete.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class ArtifactMaterialListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_material_list.html'
    model = ArtifactMaterial
    context_object_name = 'materials'


class ArtifactImageCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'


class ArtifactFormDetails(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_detail.html'
    # form_class = ArtifactFormDetails
    model = Artifact
    form_class = ArtifactForm
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'
    success_url = reverse_lazy('artifacts:images')
    form_description = _('Some Artifact Description')


class ArtifactImagesFormDetails(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_image.html'
    form_class = ArtifactFormImages
    page_title = _('Artifact Images')
    page_name = 'artifact_images'
    success_url = reverse_lazy('artifacts:list')
    form_description = _('Images of Artifact')