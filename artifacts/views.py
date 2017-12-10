from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.utils.translation import ugettext as _
from artifacts.forms import ArtifactForm, UserArtifactForm
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


class ArtifactImageCreateView(JewishDiasporaUIMixin, CreateView):
    template_name = 'artifacts/artifact_create.html'
    model = ArtifactImage
    success_url = reverse_lazy('artifacts:list')
    page_title = _('Artifact image create')
    page_name = 'artifact_image_create'
    fields = '__all__'