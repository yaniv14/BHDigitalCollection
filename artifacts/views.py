import json
from collections import OrderedDict
from json import JSONDecodeError

from django.contrib.auth import login
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils import translation
from django.utils.text import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.utils.translation import ugettext_lazy as _

from .forms import ArtifactForm, UserArtifactForm, ArtifactImageFormSet, OriginAreaForm, EmptyForm, \
    ArtifactMaterialForm, UserForm, UserArtifactImageFormSet, ArtifactTypeForm, YearForm, LocationForm, \
    ImageCroppingForm, ArtifactUpdateForm
from .models import Artifact, ArtifactStatus, ArtifactImage, PageBanner, OriginArea, ArtifactMaterial, \
    ArtifactType
from bhdigitalcollection.base_views import BHUIMixin
from users.models import User


def filter_data(request, qs, is_private):
    filters = request.GET.get('filter', None)
    if filters == 'time':
        time_from = request.GET.get('year_from', None)
        time_to = request.GET.get('year_to', None)
        if time_from and time_to:
            res = qs.filter(status=ArtifactStatus.APPROVED, is_private=is_private)
            return res.filter(year_from__gte=int(time_from)).exclude(year_to__gt=int(time_to))
    elif filters == 'location':
        location = request.GET.get('location', "")
        res = qs.filter(status=ArtifactStatus.APPROVED, is_private=is_private)
        if location.isdigit():
            loc = int(location)
        else:
            loc = 0
        return res.filter(Q(origin_country=location) | Q(origin_city_en=location) | Q(origin_city_he=location) | Q(
            origin_area_id=loc))
    return qs.filter(status=ArtifactStatus.APPROVED, is_private=is_private)


class AboutView(BHUIMixin, TemplateView):
    template_name = 'artifacts/about.html'
    page_title = _('About')
    page_name = 'about'


class PartOfTheStoryView(BHUIMixin, TemplateView):
    template_name = 'artifacts/part-of-the-story.html'
    page_title = _('Part of the story')
    page_name = 'part_of_the_story'


class HomeView(BHUIMixin, ListView):
    template_name = 'artifacts/home.html'
    page_title = _('Home')
    page_name = 'home'
    page_banner = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()
    model = Artifact
    context_object_name = 'artifacts'
    filterable = True

    def set_filter_form(self):
        filter_type = self.request.GET.get('filter', None)
        if filter_type == 'time':
            return YearForm(initial={'filter': filter_type})
        elif filter_type == 'location':
            return LocationForm(initial={'filter': filter_type}, bidi=translation.get_language_bidi())
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artifacts = Artifact.objects.filter(is_private=False)
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                artifacts = artifacts.filter(status=ArtifactStatus.APPROVED)
        else:
            artifacts = artifacts.filter(status=ArtifactStatus.APPROVED)

        context['featured'] = artifacts.filter(is_featured=True)
        context['none_featured'] = artifacts.filter(is_featured=False)
        return context


class ArtifactUsersListView(BHUIMixin, ListView):
    template_name = 'artifacts/users_artifact_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('Users artifacts list')
    page_name = 'users_artifact_list'
    page_banner = PageBanner.objects.filter(active=True, page='users_collections').order_by('?').first()
    if not page_banner:
        page_banner = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()
    filterable = True

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return qs.filter(is_private=True)
        return qs.filter(status=ArtifactStatus.APPROVED, is_private=True)

    def set_filter_form(self):
        filter_type = self.request.GET.get('filter', None)
        if filter_type == 'time':
            return YearForm(initial={'is_private': True, 'filter': filter_type})
        elif filter_type == 'location':
            return LocationForm(initial={'is_private': True, 'filter': filter_type},
                                bidi=translation.get_language_bidi())
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED, is_private=False,
                                                           is_featured=False)
        return context


class ArtifactFullListView(BHUIMixin, ListView):
    template_name = 'artifacts/artifact_full_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('All artifacts list')
    page_name = 'all_artifact_list'
    filterable = True
    page_banner = PageBanner.objects.filter(active=True, page='all_collections').order_by('?').first()
    if not page_banner:
        page_banner = PageBanner.objects.filter(active=True, page='museum_collections').order_by('?').first()

    def set_filter_form(self):
        filter_type = self.request.GET.get('filter', None)
        if filter_type == 'time':
            return YearForm(initial={'all': True, 'filter': filter_type})
        elif filter_type == 'location':
            return LocationForm(initial={'all': True, 'filter': filter_type},
                                bidi=translation.get_language_bidi())
        return None

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return qs
        return qs.filter(status=ArtifactStatus.APPROVED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['none_featured'] = Artifact.objects.filter(status=ArtifactStatus.APPROVED)
        return context


class ArtifactDetailView(BHUIMixin, DetailView):
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'

    def get_template_names(self):
        if self.object.is_private:
            return 'artifacts/user_artifact_detail.html'
        return 'artifacts/artifact_detail.html'


class ArtifactCreateStepOneView(BHUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_one.html'
    form_class = UserForm
    success_url = reverse_lazy('artifacts:create_step_two')
    page_title = _('Artifact create')
    page_name = 'artifact_create_1'

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


class ArtifactCreateStepTwoView(BHUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_two.html'
    model = Artifact
    page_title = _('Artifact create')
    page_name = 'artifact_create_2'
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
            country_area = form.cleaned_data['country_area']
            if country_area[0]:
                form.instance.origin_country = country_area[1]
            elif country_area[2]:
                form.instance.origin_area_id = country_area[3]
            period = form.cleaned_data['period']
            if period[0]:
                if period[1].isdigit():
                    form.instance.year_from = int(period[1])
                if period[2].isdigit():
                    form.instance.year_to = int(period[2])
            elif period[3]:
                if period[4].isdigit():
                    form.instance.year_from = int(period[4])
                    form.instance.year_to = int(period[4])
            form.instance.is_private = True
            form.instance.slug = slugify(form.cleaned_data['name_he'], True)
            form.instance.name_en = form.cleaned_data['name_he']
            form.instance.description_en = form.cleaned_data['description_he']
            form.instance.technical_data_en = form.cleaned_data['technical_data_he']
            form.instance.donor_name_en = form.cleaned_data['donor_name_he']

        return super().form_valid(form)


class ArtifactUpdateView(SuccessMessageMixin, BHUIMixin, UpdateView):
    template_name = 'artifacts/artifact_update.html'
    model = Artifact
    page_title = _('Artifact update')
    page_name = 'artifact_update'
    success_message = _('Update successfully')

    def get_form_class(self):
        return ArtifactUpdateForm

    def get_success_url(self):
        return reverse('artifacts:artifact_update', args=[self.get_object().id])

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user

        if self.request.user.is_superuser:
            form.instance.status = ArtifactStatus.APPROVED
        else:
            country_area = form.cleaned_data['country_area']
            if country_area[0]:
                form.instance.origin_country = country_area[1]
            elif country_area[2]:
                form.instance.origin_area_id = country_area[3]
            period = form.cleaned_data['period']
            if period[0]:
                if period[1].isdigit():
                    form.instance.year_from = int(period[1])
                if period[2].isdigit():
                    form.instance.year_to = int(period[2])
            elif period[3]:
                if period[4].isdigit():
                    form.instance.year_from = int(period[4])
                    form.instance.year_to = int(period[4])
            form.instance.is_private = True
            form.instance.slug = slugify(form.cleaned_data['name_he'], True)
            form.instance.name_en = form.cleaned_data['name_he']
            form.instance.description_en = form.cleaned_data['description_he']
            form.instance.technical_data_en = form.cleaned_data['technical_data_he']
            form.instance.donor_name_en = form.cleaned_data['donor_name_he']

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['images'] = self.get_object().images.all()
        return d


class ArtifactCreateStepThreeView(BHUIMixin, FormView):
    template_name = 'artifacts/artifact_create_step_three.html'
    page_title = _('Artifact Images')
    page_name = 'artifact_images'
    form_class = EmptyForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('home')
        return reverse_lazy('part_of_the_story')

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


class CropImageFormView(BHUIMixin, FormView):
    template_name = 'artifacts/image-crop.html'
    page_title = _('Image crop')
    page_name = 'image_crop'
    form_class = ImageCroppingForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        try:
            image_obj = ArtifactImage.objects.get(pk=int(self.kwargs['pk']))
            thumbs = image_obj.thumbnails
            if thumbs:
                d = {
                    'small_thumbnail': thumbs.get('small_thumbnail', {}),
                    'small_thumbnail_vertical': thumbs.get('small_thumbnail_vertical', {}),
                    'big_thumbnail': thumbs.get('big_thumbnail', {}),
                    'cover': thumbs.get('cover', {}),
                    'footer': thumbs.get('footer', {}),
                }
            else:
                d = {}
        except ArtifactImage.DoesNotExist:
            d = {}
        return d

    def form_valid(self, form):
        data = form.cleaned_data
        small_thumbnail_str = data.get('small_thumbnail', '{}')
        small_thumbnail_vertical_str = data.get('small_thumbnail_vertical', '{}')
        big_thumbnail_str = data.get('big_thumbnail', '{}')
        cover_str = data.get('cover', '{}')
        footer_str = data.get('footer', '{}')
        try:
            small_thumbnail = json.loads(small_thumbnail_str)
        except JSONDecodeError:
            small_thumbnail = None
        except TypeError:
            small_thumbnail = None
        try:
            small_thumbnail_vertical = json.loads(small_thumbnail_vertical_str)
        except JSONDecodeError:
            small_thumbnail_vertical = None
        except TypeError:
            small_thumbnail_vertical = None
        try:
            big_thumbnail = json.loads(big_thumbnail_str)
        except JSONDecodeError:
            big_thumbnail = None
        except TypeError:
            big_thumbnail = None
        try:
            cover = json.loads(cover_str)
        except JSONDecodeError:
            cover = None
        except TypeError:
            cover = None
        try:
            footer = json.loads(footer_str)
        except JSONDecodeError:
            footer = None
        except TypeError:
            footer = None
        image_obj = ArtifactImage.objects.get(pk=int(self.kwargs['pk']))
        thumb_dict = OrderedDict()
        if small_thumbnail:
            thumb_dict['small_thumbnail'] = [
                small_thumbnail.get('x'),
                small_thumbnail.get('y'),
                small_thumbnail.get('x') + small_thumbnail.get('width'),
                small_thumbnail.get('y') + small_thumbnail.get('height'),
            ]
        if small_thumbnail_vertical:
            thumb_dict['small_thumbnail_vertical'] = [
                small_thumbnail_vertical.get('x'),
                small_thumbnail_vertical.get('y'),
                small_thumbnail_vertical.get('x') + small_thumbnail_vertical.get('width'),
                small_thumbnail_vertical.get('y') + small_thumbnail_vertical.get('height'),
            ]
        if big_thumbnail:
            thumb_dict['big_thumbnail'] = [
                big_thumbnail.get('x'),
                big_thumbnail.get('y'),
                big_thumbnail.get('x') + big_thumbnail.get('width'),
                big_thumbnail.get('y') + big_thumbnail.get('height'),
            ]
        if cover:
            thumb_dict['cover'] = [
                cover.get('x'),
                cover.get('y'),
                cover.get('x') + cover.get('width'),
                cover.get('y') + cover.get('height'),
            ]
        if footer:
            thumb_dict['footer'] = [
                footer.get('x'),
                footer.get('y'),
                footer.get('x') + footer.get('width'),
                footer.get('y') + footer.get('height'),
            ]
        image_obj.thumbnails = thumb_dict
        image_obj.save()
        image_obj.generate_thumbnails()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        try:
            obj = ArtifactImage.objects.get(pk=int(self.kwargs['pk']))
            d['image'] = obj.image.url
            d['object'] = obj.thumbnails
        except ArtifactImage.DoesNotExist:
            d['object'] = None

        return d


class OriginAreaDeleteView(BHUIMixin, DeleteView):
    template_name = 'artifacts/origin_area_delete.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area delete')
    page_name = 'origin_area_delete'


class OriginAreaCreateView(BHUIMixin, CreateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area create')
    page_name = 'origin_area_create'


class OriginAreaUpdateView(BHUIMixin, UpdateView):
    template_name = 'artifacts/origin_area_create.html'
    model = OriginArea
    form_class = OriginAreaForm
    success_url = reverse_lazy('artifacts:origin_area_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class OriginAreaListView(BHUIMixin, ListView):
    template_name = 'artifacts/origin_area_list.html'
    model = OriginArea
    context_object_name = 'areas'
    page_title = _('Origin area list')
    page_name = 'origin_area_list'


class ArtifactMaterialCreateView(BHUIMixin, CreateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material create')
    page_name = 'artifact_material_create'


class ArtifactMaterialUpdateView(BHUIMixin, UpdateView):
    template_name = 'artifacts/artifact_material.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Artifact material update')
    page_name = 'artifact_material_update'


class ArtifactMaterialDeleteView(BHUIMixin, DeleteView):
    template_name = 'artifacts/artifact_material_delete.html'
    model = ArtifactMaterial
    form_class = ArtifactMaterialForm
    success_url = reverse_lazy('artifacts:material_list')
    page_title = _('Origin area update')
    page_name = 'origin_area_update'


class ArtifactMaterialListView(BHUIMixin, ListView):
    template_name = 'artifacts/artifact_material_list.html'
    model = ArtifactMaterial
    context_object_name = 'materials'


class ArtifactTypeCreateView(BHUIMixin, CreateView):
    template_name = 'artifacts/artifact_type.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type create')
    page_name = 'artifact_type_create'


class ArtifactTypeUpdateView(BHUIMixin, UpdateView):
    template_name = 'artifacts/artifact_type.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type update')
    page_name = 'artifact_type_update'


class ArtifactTypeDeleteView(BHUIMixin, DeleteView):
    template_name = 'artifacts/artifact_type_delete.html'
    model = ArtifactType
    form_class = ArtifactTypeForm
    success_url = reverse_lazy('artifacts:type_list')
    page_title = _('Artifact type delete')
    page_name = 'artifact_type_delete'


class ArtifactTypeListView(BHUIMixin, ListView):
    template_name = 'artifacts/artifact_type_list.html'
    model = ArtifactType
    context_object_name = 'types'


class ArtifactImageCreateView(BHUIMixin, CreateView):
    template_name = 'artifacts/artifact_create_step_one.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'


class ArtifactFilterView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        filter = self.request.GET.get('filter')
        location = self.request.GET.get('location')
        is_private = self.request.GET.get('is_private')
        all_artifacts = self.request.GET.get('all')
        year_from = self.request.GET.get('year_from')
        year_to = self.request.GET.get('year_to')
        if filter:
            artifacts = Artifact.objects.filter(status=ArtifactStatus.APPROVED,
                                                is_private=True if is_private else False)
            user_artifacts = artifacts
            none_featured = artifacts.filter(is_featured=False)
            artifacts = artifacts.filter(is_featured=True)
            if location:
                artifacts = artifacts.filter(origin_area_id=int(location))
                user_artifacts = user_artifacts.filter(origin_area_id=int(location))
                none_featured = none_featured.filter(origin_area_id=int(location))
            elif year_from and year_to:
                artifacts = artifacts.filter(year_from__gte=int(year_from)).exclude(year_to__gt=int(year_to))
                user_artifacts = user_artifacts.filter(year_from__gte=int(year_from)).exclude(year_to__gt=int(year_to))
                none_featured = none_featured.filter(year_from__gte=int(year_from)).exclude(year_to__gt=int(year_to))
        else:
            none_featured = Artifact.objects.none()
            artifacts = Artifact.objects.none()
            user_artifacts = Artifact.objects.none()

        if is_private:
            return render(request, 'artifacts/_user_artifacts.html', {'artifacts': user_artifacts})
        if all_artifacts:
            return render(request, 'artifacts/_full_artifacts.html', {'artifacts': Artifact.objects.all()})
        return render(request, 'artifacts/_artifacts.html', {'artifacts': artifacts, 'none_featured': none_featured})
