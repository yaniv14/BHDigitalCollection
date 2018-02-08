from django.urls import path, re_path
from . import views


app_name = 'artifacts'

urlpatterns = [
    path('users/', views.ArtifactUsersListView.as_view(), name='users'),
    path('all/', views.ArtifactFullListView.as_view(), name='all_artifacts'),
    re_path('(?P<slug>[-\w]+)/', views.ArtifactDetailView.as_view(), name='detail'),
    path('create/step/one/', views.ArtifactCreateStepOneView.as_view(), name='create_step_one'),
    path('create/step/two/', views.ArtifactCreateStepTwoView.as_view(), name='create_step_two'),
    path('<int:pk>/create/step/three/', views.ArtifactCreateStepThreeView.as_view(), name='create_step_three'),
    path('area/list/', views.OriginAreaListView.as_view(), name='origin_area_list'),
    path('area/create/', views.OriginAreaCreateView.as_view(), name='origin_area_create'),
    path('area/update/<int:pk>/', views.OriginAreaUpdateView.as_view(), name='origin_area_update'),
    path('area/delete/<int:pk>/', views.OriginAreaDeleteView.as_view(), name='origin_area_delete'),
    path('material/list/', views.ArtifactMaterialListView.as_view(), name='material_list'),
    path('material/create/', views.ArtifactMaterialCreateView.as_view(), name='material_create'),
    path('material/update/<int:pk>/', views.ArtifactMaterialUpdateView.as_view(), name='material_update'),
    path('material/delete/<int:pk>/', views.ArtifactMaterialDeleteView.as_view(), name='material_delete'),
    path('type/list/', views.ArtifactTypeListView.as_view(), name='type_list'),
    path('type/create/', views.ArtifactTypeCreateView.as_view(), name='type_create'),
    path('type/update/<int:pk>/', views.ArtifactTypeUpdateView.as_view(), name='type_update'),
    path('type/delete/<int:pk>/', views.ArtifactTypeDeleteView.as_view(), name='type_delete'),
    path('image/create/', views.ArtifactImageCreateView.as_view(), name='image_create'),
]
