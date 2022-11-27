from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import ProjectForm
from .models import Project, Review, Tag


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'


# def projects(request):
#     projects = Project.objects.all()
#     context = {'projects': projects}
#     return render(request, 'projects/projects.html', context)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/single-project.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projectObj = Project.objects.get(id=self.kwargs['pk'])
        context['project'] = projectObj
        return context


# def project(request, pk):
#     projectObj = Project.objects.get(id=pk)
#     return render(request, 'projects/single-project.html', {'project': projectObj})


def createProject(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects')
    return render(request, 'projects/project_form.html', {'form': form})
