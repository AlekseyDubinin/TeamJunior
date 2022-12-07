from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.urls import conf, reverse_lazy
from django.views.generic import CreateView, ListView

from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm


class MyLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login_register.html'
    # success_url = reverse_lazy('account')
    success_message = 'Вы успешно вошли в систему'

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)

    # def get_success_url(self):



    # def post(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('profiles')
    #
    #     if request.method == 'POST':
    #         username = request.POST['username']
    #         password = request.POST['password']
    #
    #         try:
    #             user = User.objects.get(username=username)
    #         except:
    #             messages.error(request, 'Такого пользователя нет в системе')
    #
    #         user = authenticate(request, username=username, password=password)
    #
    #         if user is not None:
    #             login(request, user)
    #             return redirect(
    #                 request.GET['next'] if 'next' in request.GET else 'account')
    #
    #         else:
    #             messages.error(request, 'Неверное имя пользователя или пароль')
    #
    #     return render(request, 'users/login_register.html')



def logoutUser(request):
    logout(request)
    messages.info(request, 'Вы вышли из учетной записи')
    return redirect('login')


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/login_register.html'
    success_url = reverse_lazy('edit-account')
    messages.success = 'Аккаунт успешно создан!'
    extra_context = {
        'page': 'register'
    }  # чтобы попасть на форму регистрации

    def form_valid(self, form):
        user = form.save()
        user.username = user.username.lower()
        user.save()
        Profile.objects.create(user=user,
                               name=user.first_name,
                               email=user.email,
                               username=user.username)
        login(self.request, user)
        return redirect(self.success_url)



# def registerUser(request):
#     page = 'register'
#     form = CustomUserCreationForm()
#
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()
#             Profile.objects.create(user=user,
#                                    name=user.first_name,
#                                    email=user.email,
#                                    username=user.username)
#
#             messages.success(request, 'Аккаунт успешно создан!')
#
#             login(request, user)
#             return redirect('edit-account')
#
#         else:
#             messages.success(
#                 request, 'Во время регистрации возникла ошибка')
#
#     context = {'page': page, 'form': form}
#     return render(request, 'users/login_register.html', context)

class Profiles(ListView):
    queryset = Profile.objects.all()
    template_name = "users/profiles.html"
    extra_context = {
        'profiles': queryset
    }


# def profiles(request):
#     profiles = Profile.objects.all()
#     context = {'profiles': profiles}
#     return render(request, 'users/profiles.html', context)


def userProfile(request, id):
    profile = Profile.objects.get(id=id)

    main_skills = profile.skills.all()[:2]
    extra_skills = profile.skills.all()[2:]

    context = {'profile': profile, 'main_skills': main_skills,
               "extra_skills": extra_skills}
    return render(request, 'users/user-profile.html', context)

def profiles_by_skill(request, skill_slug):
    skill = get_object_or_404(Skill, slug=skill_slug)
    profiles = Profile.objects.filter(skills__in=[skill])
    context = {
        "profiles": profiles
    }

    return render(request, "users/profiles.html", context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skills.all()
    projects = profile.project_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill_slug = request.POST.get('slug')
            skill_description = request.POST.get('description')
            profile.skills.get_or_create(name=skill, slug=skill_slug, description=skill_description)
            messages.success(request, 'Навык добавлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, skill_slug):
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Навык успешно обновлен')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, skill_slug):
    profile = request.user.profile
    skill = profile.skills.get(slug=skill_slug)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Навык успешно удален')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', id=pk)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)

