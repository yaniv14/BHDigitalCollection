from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.utils.translation import ugettext as _
from artifacts.forms import ArtifactForm, UserArtifactForm, ArtifactImageFormSet
from artifacts.models import Artifact, ArtifactStatus, ArtifactImage
from jewishdiaspora.base_views import JewishDiasporaUIMixin


class HomeView(JewishDiasporaUIMixin, TemplateView):
    template_name = 'artifacts/home.html'
    page_title = _('Home')
    page_name = 'home'


class ArtifactListView(JewishDiasporaUIMixin, ListView):
    template_name = 'artifacts/artifact_list.html'
    model = Artifact
    context_object_name = 'artifacts'
    page_title = _('Artifacts list')
    page_name = 'artifact_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return super(ArtifactListView, self).get_queryset()

        return super(ArtifactListView, self).get_queryset().filter(status=ArtifactStatus.APPROVED, is_private=False)


class ArtifactDetailView(JewishDiasporaUIMixin, DetailView):
    template_name = 'artifacts/artifact_detail.html'
    model = Artifact
    context_object_name = 'artifact'
    page_title = _('Artifact detail')
    page_name = 'artifact_detail'


class ArtifactCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create.html'
    model = Artifact
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact create')
    page_name = 'artifact_create'

    def get_form_class(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return ArtifactForm

        return UserArtifactForm

    def form_valid(self, form):
        context = self.get_context_data()
        artifact_image_formset = context['artifact_image_formset']

        if artifact_image_formset.is_valid():
            if self.request.user.is_authenticated:
                form.instance.uploaded_by = self.request.user
                if not self.request.user.is_superuser:
                    form.instance.is_private = True
            self.object = form.save()
            artifact_image_formset.instance = self.object
            artifact_image_formset.save()
            return super().form_valid(form)
            # return redirect(self.success_url)

        return super().form_invalid(form)
        # return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ArtifactCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['artifact_image_formset'] = ArtifactImageFormSet(self.request.POST, self.request.FILES, prefix='artifact_image_formset')
        else:
            context['artifact_image_formset'] = ArtifactImageFormSet(prefix='artifact_image_formset')
        return context


class ArtifactImageCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'