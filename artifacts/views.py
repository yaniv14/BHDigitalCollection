import pdb

from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.utils.translation import ugettext_lazy as _

from artifacts.forms import ArtifactForm, UserArtifactForm, ArtifactImageFormSet, OriginAreaForm, EmptyForm, \
    ArtifactMaterialForm, UserForm, UserArtifactImageFormSet, ArtifactTypeForm, YearForm, LocationForm
from artifacts.models import Artifact, ArtifactStatus, ArtifactImage, PageBanner, OriginArea, ArtifactMaterial, \
    ArtifactType
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


def get_custom_context_data(self, context):
    filters = self.request.GET.get('filter', None)
    context['filters'] = filters
    year_form = YearForm(self.request.GET)
    location_form = LocationForm(self.request.GET)
    if filters == 'time':
        pass
    elif filters == 'location':
        pass
    context['filter_form'] = year_form
    context['location_form'] = location_form
    context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED, is_private=False,
                                                       is_featured=False)
    context['page_banner'] = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()


def set_filters(self, context):
    filters = self.request.GET.get('filter', None)
    context['filters'] = filters
    year_form = YearForm(self.request.GET)
    location_form = LocationForm(self.request.GET)
    if filters == 'time':
        pass
    elif filters == 'location':
        pass
    context['filter_form'] = year_form
    context['location_form'] = location_form


def filter_data(self, mixin, is_private):
    filters = self.request.GET.get('filter', None)
    if filters == 'time':
        time_from = self.request.GET.get('year_from', None)
        time_to = self.request.GET.get('year_to', None)
        if time_from and time_to:
            qs = mixin.get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=is_private)
            return qs.filter(year_from__gte=int(time_from)).exclude(year_to__gt=int(time_to))
    elif filters == 'location':
        location = self.request.GET.get('location', "")
        qs = mixin.get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=is_private)
        if location.isdigit():
            loc = int(location)
        else:
            loc = 0
        return qs.filter(Q(origin_country=location) | Q(origin_city_en=location) | Q(origin_city_he=location) | Q(
            origin_area_id=loc))
    return mixin.get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=is_private)


class HomeView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/home.html'
    page_title = _('Home')
    page_name = 'home'
    model = Artifact
    context_object_name = 'artifacts'
    filterable = True

    def get_queryset(self):
        return filter_data(self, super(JewishDiasporaUIMixin, self), False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_filters(self, context)
        context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED, is_private=False,
                                                           is_featured=False)
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
    filterable = True

    def get_queryset(self):
        return filter_data(self, super(JewishDiasporaUIMixin, self), True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        set_filters(self, context)
        context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED, is_private=False,
                                                           is_featured=False)
        context['page_banner'] = PageBanner.objects.filter(active=True, page='users_collections').order_by('?').first()
        return context


class ArtifactFullListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_full_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('All artifacts list')
    page_name = 'all_artifact_list'
    filterable = True

    def get_queryset(self):
        return filter_data(self, super(JewishDiasporaUIMixin, self), False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        set_filters(self, context)
        context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED, is_private=False,
                                                           is_featured=True)
        context['page_banner'] = PageBanner.objects.filter(active=True, page='all_collections').order_by('?').first()
        return context


class ArtifactDetailView(JewishDiasporaUIMixin, DetailView):
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'

    def get_template_names(self):
        if self.object.is_private:
            return 'artifacts/user_artifact_detail.html'
        return 'artifacts/artifact_detail.html'


class ArtifactCreateStepOneView(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_one.html'
    form_class = UserForm
    success_url = reverse_lazy('artifacts:create_step_two')
    page_title = _('Artifact create')
    page_name = 'artifact_create'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'logged': self.request.user.is_authenticated,
            'bidi': translation.get_language_bidi()
        })
        return kwargs

    def get_initial(self):
        if self.request.user.is_authenticated:
            return {
                'name': self.request.user.full_name,
                'email': self.request.user.email,
                'phone_number': self.request.user.phone,
            }

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone_number')

        if not self.request.user.is_authenticated:
            password = User.objects.make_random_password()
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=name,
                phone=phone
            )
            # Send email
            user.send_registration_email(password)
            # Login user into session
            login(self.request, user)

        return super().form_valid(form)


class ArtifactCreateStepTwoView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_two.html'
    model = Artifact
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'
    form_description = _('Some Artifact Description')

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('artifacts:create_step_one'))
        return super().get(request, *args, **kwargs)

    def get_initial(self):
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            return {
                'donor_name_he': self.request.user.full_name,
                'donor_name_en': self.request.user.full_name,
            }

    def get_form_class(self):
        if self.request.user.is_superuser:
            return ArtifactForm
        else:
            return UserArtifactForm

    def get_success_url(self):
        return reverse('artifacts:create_step_three', args=[self.object.id])

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user

        if self.request.user.is_superuser:
            form.instance.status = ArtifactStatus.APPROVED
        else:
            form.instance.is_private = True
            form.instance.slug = slugify(form.cleaned_data['name_he'], True)
            form.instance.name_en = form.cleaned_data['name_he']
            form.instance.description_en = form.cleaned_data['description_he']
            form.instance.technical_data_en = form.cleaned_data['technical_data_he']
            form.instance.donor_name_en = form.cleaned_data['donor_name_he']

        return super().form_valid(form)


class ArtifactCreateStepThreeView(JewishDiasporaUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_three.html'
    page_title = _('Artifact Images')
    page_name = 'artifact_images'
    success_url = reverse_lazy('home')
    form_class = EmptyForm

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('artifacts:create_step_one'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()
        artifact_image_formset = context['artifact_image_formset']

        if artifact_image_formset.is_valid():
            artifact = Artifact.objects.get(pk=self.kwargs['pk'])
            if not self.request.user.is_superuser:
                for image_form in artifact_image_formset:
                    image_form.instance.description_en = image_form.cleaned_data.get('description_he')
                    image_form.instance.credit_en = image_form.cleaned_data.get('credit_he')
                    image_form.instance.year_era_en = image_form.cleaned_data.get('year_era_he')
                    image_form.instance.location_en = image_form.cleaned_data.get('location_he')
            artifact_image_formset.instance = artifact
            artifact_image_formset.save()

            return super().form_valid(form)

        # return self.render_to_response(context)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['artifact_image_formset'] = ArtifactImageFormSet(
                self.request.POST, self.request.FILES, prefix='artifact_image_formset'
            ) if self.request.user.is_superuser else UserArtifactImageFormSet(
                self.request.POST, self.request.FILES, prefix='artifact_image_formset'
            )
        else:
            context['artifact_image_formset'] = ArtifactImageFormSet(
                prefix='artifact_image_formset'
            ) if self.request.user.is_superuser else UserArtifactImageFormSet(
                prefix='artifact_image_formset'
            )
        return context


class OriginAreaDeleteView(JewishDiasporaUIMixin, DeleteView):
    template_name = 'artifacts/origin_area_delete.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area delete')
    page_name = 'origin_area_delete'


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


class ArtifactTypeCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_type.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type create')
    page_name = 'artifact_type_create'


class ArtifactTypeUpdateView(JewishDiasporaUIMixin, UpdateView):
    template_name = 'artifacts/artifact_type.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type update')
    page_name = 'artifact_type_update'


class ArtifactTypeDeleteView(JewishDiasporaUIMixin, DeleteView):
    template_name = 'artifacts/artifact_type_delete.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type delete')
    page_name = 'artifact_type_delete'


class ArtifactTypeListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_type_list.html'
    model = ArtifactType
    context_object_name = 'types'


class ArtifactImageCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_one.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'
