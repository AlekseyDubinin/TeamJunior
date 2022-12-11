from django.urls import path
from . import views


urlpatterns = [

    path('', views.ProfilesListView.as_view(), name="profiles"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterUserView.as_view(), name="register"),
    path('profile/<uuid:pk>/', views.UserProfileView.as_view(), name="user-profile"),
    path('account/', views.UserAccountView.as_view(), name="account"),
    path('edit-account/', views.AccountUpdateView.as_view(), name="edit-account"),
    path('create-skill/', views.SkillCreateView.as_view(), name="create-skill"),
    path('update-skill/<slug:skill_slug>/', views.SkillUpdateView.as_view(), name="update-skill"),
    path('delete-skill/<slug:skill_slug>/', views.SkillDeleteView.as_view(), name="delete-skill"),
    # path('skill/<slug:skill_slug>', views.profiles_by_skill, name="skill"),
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<uuid:pk>/', views.createMessage, name="create-message"),

]
