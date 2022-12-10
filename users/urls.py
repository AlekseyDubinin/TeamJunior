from django.urls import path
from . import views


urlpatterns = [

    path('', views.Profiles.as_view(), name="profiles"),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('profile/<uuid:pk>/', views.UserProfile.as_view(), name="user-profile"),
    path('account/', views.UserAccount.as_view(), name="account"),
    path('edit-account/', views.EditAccount.as_view(), name="edit-account"),
    path('create-skill/', views.CreateSkill.as_view(), name="create-skill"),
    path('update-skill/<slug:skill_slug>/', views.updateSkill, name="update-skill"),
    path('delete-skill/<slug:skill_slug>/', views.deleteSkill, name="delete-skill"),
    # path('skill/<slug:skill_slug>', views.profiles_by_skill, name="skill"),
    path('inbox/', views.inbox, name="inbox"),
    path('message/<str:pk>/', views.viewMessage, name="message"),
    path('create-message/<uuid:pk>/', views.createMessage, name="create-message"),

]
