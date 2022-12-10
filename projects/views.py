from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core import paginator
from .utils import PaG

from .forms import ProjectForm, ReviewForm
from .models import Project, Review, Tag


class ProjectListView(ListView):
    paginate_by = 3
    model = Project

    template_name = 'projects/projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        projects = Project.objects.all()
        search_query = self.request.GET.get('search_query')

        if search_query:
            projects = projects.distinct().filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(owner__name__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            )

        return projects



# def projects(request):
#     projects = Project.objects.all()
#     context = {'projects': projects}
#     return render(request, 'projects/projects.html', context)


# class ProjectDetailView(DetailView):
#     model = Project
#     template_name = 'projects/single-project.html'
#     context_object_name = 'project'

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     projectObj = Project.objects.get(id=self.kwargs['pk'])
#     context['project'] = projectObj
#     return context


# def project(request, pk):
#     projectObj = Project.objects.get(id=pk)
#     return render(request, 'projects/single-project.html', {'project': projectObj})


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


# class ProjectCreateView(CreateView):
#     model = Project
#     template_name = 'projects/project_form.html'
#     form_class = ProjectForm
#     success_url = reverse_lazy('projects')

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
    success_url = reverse_lazy('account')

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        newtags = request.POST.get('newtags').replace(',', " ").split()
        if self.form_valid:
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                self.object.tags.add(tag)
            return redirect(self.success_url)

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
    template_name = 'delete_template.html'
    success_url = reverse_lazy('account')


# def deleteProject(request, pk):
#     project = Project.objects.get(id=pk)
#     if request.method == 'POST':
#         project.delete()
#         return redirect('projects')
#     context = {'object': project}
#     return render(request, 'projects/delete.html', context)

"""
Так же как и с фильтрацией профилей по скиллам заменил ссылку в шаблоне на фильтрацию проектов

def projects_by_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects = Project.objects.filter(tags__in=[tag])
    context = {
        "projects": projects
    }

    return render(request, "projects/projects.html", context)
"""



def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount
        messages.info(request, 'Ваш отзыв был добавлен!')
        return redirect('project', pk=project.id)
    return render(request, 'projects/single-project.html', {'project': project, 'form': form})
