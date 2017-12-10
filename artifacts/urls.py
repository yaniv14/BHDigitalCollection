from django.urls import path
from . import views


app_name = 'artifacts'

urlpatterns = [
    path('list/', views.ArtifactListView.as_view(), name='list'),
    path('<int:pk>/', views.ArtifactDetailView.as_view(), name='detail'),
    path('create/', views.ArtifactCreateView.as_view(), name='create'),
    path('image/create/', views.ArtifactImageCreateView.as_view(), name='image_create'),
]
