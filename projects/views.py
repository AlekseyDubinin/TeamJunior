from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     projectObj = Project.objects.get(id=self.kwargs['pk'])
    #     context['project'] = projectObj
    #     return context


# def project(request, pk):
#     projectObj = Project.objects.get(id=pk)
#     return render(request, 'projects/single-project.html', {'project': projectObj})


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    # def form_valid(self, form):
    #     form.save()
    #     return redirect('projects')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


# def createProject(request):
#     form = ProjectForm()
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('projects')
#     return render(request, 'projects/project_form.html', {'form': form})


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'projects/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects')

    # def form_valid(self, form):
    #     form.save()
    #     return redirect('projects')

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


# def updateProject(request, pk):
#     project = Project.objects.get(id=pk)
#     form = ProjectForm(instance=project)
#     if request.method == 'POST':
#         form = ProjectForm(request.POST, instance=project)
#         if form.is_valid():
#             form.save()
#             return redirect('projects')
#     context = {'form': form}
#     return render(request, 'projects/project_form_update.html', context)



class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'projects/delete.html'
    success_url = reverse_lazy('projects')

# def deleteProject(request, pk):
#     project = Project.objects.get(id=pk)
#     if request.method == 'POST':
#         project.delete()
#         return redirect('projects')
#     context = {'object': project}
#     return render(request, 'projects/delete.html', context)


def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    context = {
        "projects": projects
    }

    return render(request, "projects/projects.html", context)

