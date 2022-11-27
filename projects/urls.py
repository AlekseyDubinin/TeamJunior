from django.urls import path
from .views import ProjectListView, ProjectDetailView, createProject
urlpatterns = [
    path('', ProjectListView.as_view(), name="projects"),
    path('project-object/<str:pk>/', ProjectDetailView.as_view(), name="project"),
    path('create-project/', createProject, name="create-project"),
]