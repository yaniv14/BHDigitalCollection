from django.urls import path
from . import views


app_name = 'artifacts'

urlpatterns = [
    path('users/', views.ArtifactUsersListView.as_view(), name='users'),
    path('<int:pk>/', views.ArtifactDetailView.as_view(), name='detail'),
    path('create/', views.ArtifactCreateView.as_view(), name='create'),
    path('new/', views.TheNewForm.as_view(), name='artifacts_donors_registration'),
    path('personal_info/', views.PersonalInformationRegistrationPage.as_view(), name='PersonalInformationRegistrationPage'),
    path('artifact_info/', views.ArtifactInformationRegistrationPage.as_view(), name='ArtifactInformationRegistrationPage'),
    path('artifact_images/', views.ArtifactsImagesRegistrationPage.as_view(), name='ArtifactsImagesRegistrationPage'),
    path('image/create/', views.ArtifactImageCreateView.as_view(), name='image_create'),
]
