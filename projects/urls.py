from django.urls import path
from .views import ProjectListView, ProjectDetailView, createProject, ProjectUpdateView, ProjectDeleteView, projects_by_tag
urlpatterns = [
    path('', ProjectListView.as_view(), name="projects"),
    path('project-object/<uuid:pk>/', ProjectDetailView.as_view(), name="project"),
    path('create-project/', createProject, name="create-project"),
    path('update-project/<str:pk>/', ProjectUpdateView.as_view(), name="update-project"),
    path('delete-project/<str:pk>', ProjectDeleteView.as_view(), name="delete-project"),
    path('tag/<slug:tag_slug>', projects_by_tag, name="tag"),
]
